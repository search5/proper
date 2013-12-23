# -*- coding: utf-8 -*-
from flask import Flask, abort, g, render_template, request, redirect, url_for
import sys
import os
import os.path
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
from werkzeug import secure_filename
import util

app = Flask(__name__)
app.config['UPLOAD_DIR'] = os.path.join(os.path.dirname(__file__), "uploads")

def connect_db():
    return MySQLdb.connect(host="localhost", user="sc_it", passwd="1234", db="sc_it", use_unicode=True, charset="utf8")


@app.before_request
def before_request():
    g.db = connect_db()
    remote_addr = request.remote_addr
    # 모든 연결은 세이브더칠드런 본부 혹은 로컬에서만 접속 가능해야 한다.
    # TODO : 옥산빌딩
    remote_first_addr = remote_addr[:remote_addr.rfind(".") + 1]

    # 접속 허용이 가능한 IP입니까?
    #if remote_first_addr not in ("127.0.0.", "121.131.33."):
    #    abort(403)


@app.route("/")
def main():
    return render_template("index.html")


@app.errorhandler(403)
def page_not_allow(e):
    return render_template('error/403.html'), 403


@app.route("/asset")
def asset_list():
    return render_template("asset/list.html")


@app.route("/pc", endpoint='pc')
def pc_list():

    # PC 목록 수 가져오기
    cursor = g.db.cursor()
    cursor.execute("select count(no) from pc_asset")
    total_cnt = cursor.fetchone()[0]

    ########### 페이징 정보 계산하기
	
	# 페이지 당 보여줄 목록 개수
    perPage = 12
	
	# 현재 페이지 수
    currPage = int(request.args.get('page', 1))
	
    paging_env = util.paging_env_calc(perPage, currPage, total_cnt)
    
    total_page = paging_env['totalPage']
    limitStart = paging_env['limitStart']
    prev_page_number = paging_env['prevPageNum']
    next_page_number = paging_env['nextPageNum']

    # 단, 현재 페이지 수(요청받은 페이지 번호)가 전체 페이지 수보다 큰 경우
    # 전체 페이지 수를 현재 페이지 수에 설정한다.
    if currPage > total_page:
        currPage = total_page

    ########### // 페이징 정보 계산하기

    cursor.execute("select no, code, model_nm, make_date, acquire_date, processor, memory, note from pc_asset order by no desc limit %(limitStart)d, %(perPage)d" % dict(limitStart=limitStart, perPage=perPage))
    lstPc = [dict(no=row[0], code=row[1], model_nm=row[2], make_date=row[3], acquire_date=row[4], processor=row[5], memory=row[6], note=row[7]) for row in cursor.fetchall()]

    # 커서 삭제
    del cursor

    # view에 넘길 데이터 지정
    view_data = {
        "lst_pc": lstPc,
        "total_page": int(total_page),
        "currPage": currPage,
        "prev_page_number": prev_page_number,
        "next_page_number": next_page_number
    }

    return render_template("asset/pc_list.html", **view_data)

@app.route("/pc/add/form", methods=("GET",))
def pc_asset_add_form():
    return render_template("asset/pc_add.html")

@app.route("/pc/add", methods=("POST",))
def pc_asset_add():

    ins_values = {
        "code": request.form.get("code", ""),
        "model_nm": request.form.get("model_nm", ""),
        "make_date": request.form.get("make_date", ""),
        "acquire_date": request.form.get("acquire_date", ""),
        "processor": request.form.get("processor", ""),
        "memory": request.form.get("memory", ""),
        "note": request.form.get("note", "")
    }

    ins_sql = unicode("insert into pc_asset (code, model_nm, make_date, acquire_date, processor, memory, note) values ('%(code)s', '%(model_nm)s', '%(make_date)s', '%(acquire_date)s', '%(processor)s', '%(memory)s', '%(note)s')" % ins_values)

    cursor = g.db.cursor()
    cursor.execute(ins_sql)

    del cursor

    if request.files['xml']:
        request.files['xml'].save(os.path.join(app.config['UPLOAD_DIR'], util.generateTimeBaseFileName(request.files['xml'].filename)))
    
    # XML 파일을 분석해서 정보 채워넣기

    return redirect(url_for('pc'))

@app.route("/pc/<asset_code>")
def pc_asset_view(asset_code):
    # PC 데이터 가져오기
    cursor = g.db.cursor()
    cursor.execute("select no, code, model_nm, make_date, acquire_date, processor, memory, note, addtion, windows_version, windows_key from pc_asset where code='%s'" % asset_code)
    record = cursor.fetchone()

    view_data = {
        "no": record[0],
        "code": record[1],
        "model_nm": record[2],
        "make_date": record[3],
        "acquire_date": record[4],
        "processor": record[5],
        "memory": record[6],
        "note": record[7],
        "addtion": record[8],
        "win_ver": record[9],
        "win_key": record[10]
    }

    del cursor

    return render_template("asset/pc_view.html", **view_data)

@app.teardown_request
def teardown_request(exception):
    g.db.commit()
    g.db.close()