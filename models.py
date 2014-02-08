#-*- coding: utf-8 -*-
from proper import db
import datetime
from sqlalchemy.ext.hybrid import hybrid_property

from dateutil.parser import parse

class Asset(db.Model):
    seq = db.Column(db.Integer, db.Sequence('asset_seq'), primary_key=True) # 일련번호
    asset_code = db.Column(db.String(20), unique=True) # 자산코드
    acquire_date = db.Column(db.Date) # 취득년월일
    acquire_money = db.Column(db.Integer) # 취득가
    disuse_date = db.Column(db.Date) # 폐기일
    disuse_note = db.Column(db.Text) # 폐기사유
    make_date = db.Column(db.String(20)) # 제조년월
    scan_time = db.Column(db.DateTime) # 최종검사일
    os = db.Column(db.String(100)) # 운영체제명
    service_pack = db.Column(db.String(100)) # 서비스팩 버전
    usb_support_type = db.Column(db.String(30)) # USB Support Version
    manufacture = db.Column(db.String(100)) # 제조사
    product_name = db.Column(db.String(100)) # PC 모델명
    product_serial = db.Column(db.String(100)) # PC Serial
    processor_version = db.Column(db.String(200)) # CPU Name
    memory_size = db.Column(db.String(100)) # 총 메모리 크기
    video_chip = db.Column(db.String(200)) # 비디오 칩셋
    hdd_name = db.Column(db.String(200)) # 하드 디스크 이름
    hdd_serial = db.Column(db.String(100)) # 하드 디스크 시리얼
    hdd_capacity = db.Column(db.String(100)) # 하드 디스크 용량
    mac_address = db.Column(db.String(50)) # 맥 어드레스
    asset_type = db.Column(db.String(20)) # PC 타입 여부(노트북인지, 데스크탑인지, 모니터인지 - Notebook, Desktop, Monitor)
    windows_version = db.Column(db.String(100)) # 번들 윈도우 버전
    windows_serial = db.Column(db.String(100)) # 번들 윈도우 시리얼
    config_no = db.Column(db.String(100)) # Config No (LG 데스크탑에만 존재)
    netbios_name = db.Column(db.String(100)) # 컴퓨터명(NetBIOS)
    xml_file_name = db.Column(db.String(100)) # XML 파일명(초기 매핑을 위한 고육지책) - 정리작업이 완료되면 더 쓸것 같진 않음
    xml_file_content = db.Column(db.Text) # XML 파일 내용
    note = db.Column(db.Text) # 비고
    send_date = db.Column(db.Date) # 지급일
    collect_date = db.Column(db.Date) # 회수일
    user_seq = db.Column(db.Integer, db.ForeignKey('user.seq'))
    user = db.relationship('User', backref=db.backref('assets', lazy='dynamic'))

    def __sub__(self, other_dict):
        # 사용자가 이 객체에서 마이너스 연산을 수행한 객체가 사전이 아니면 None을 반환하고 끝낸다.
        if not isinstance(other_dict, dict):
            return None

        # 변동내역을 담아둘 리스트을 생성한다.
        dict_changed_log = []

        # 사용자로부터 넘어온 값들의 키를 먼저 뽑아낸다(예, mac_address, coonfig_no 등)
        user_input_keys = other_dict.keys()

        # 사용자가 입력한 값과 레코드 값을 비교하여 변경되었으면 값의 변동 내역을 사전에 담아두고 현재 레코드에 변동 내역을 기록한다.
        # 이 때 사용자가 넘긴 user_inputed_keys의 값은 레코드 항목의 이름과 동일해야 한다.
        for item in user_input_keys:
            # 생각해보니 여기에는 User에 대한 매핑도 생각해두어야 한다. 아 젠장!
            # record 값을 얻어올 때 데이터베이스 레코드 컬럼의 값이 None인 경우를 위해서 or 연산을 해둔다.
            record_value = getattr(self, item) or ''
            user_input_value = other_dict[item]

            # 레코드값이 날짜형인 경우 user_input_value도 날짜형으로 다뤄져야 한다.
            # 이렇게 안하면 날짜형은 계속해서 히스토리 데이터가 쌓이게 된다.
            if type(record_value) == datetime.date:
                user_input_value = parse(user_input_value).date()

            # 레코드값이 숫자형인 경우 user_input_value도 숫자형으로 다뤄져야 한다.
            if type(record_value) == int:
                user_input_value = int(user_input_value)

            # 레코드값과 입력된 값이 다르면
            if record_value != user_input_value:
                dict_changed_log.append({
                    "field_name": item,
                    "old_value": record_value,
                    "new_value": user_input_value
                })

                # 새로운 값으로 변경
                setattr(self, item, user_input_value)

        return dict_changed_log

class Dept(db.Model):
    seq = db.Column(db.Integer, db.Sequence('dept_seq'), primary_key=True)
    dept_team_nm = db.Column(db.String(50)) # 부서명과 팀명 조합

    def __init__(self, name):
        self.dept_team_nm = name

class User(db.Model):
    seq = db.Column(db.Integer, db.Sequence('user_seq'), primary_key=True)
    dept_seq = db.Column(db.Integer, db.ForeignKey('dept.seq')) # 팀 코드
    user_name = db.Column(db.String(20)) # 사용자명
    user_position = db.Column(db.String(30)) # 직급
    user_ip = db.Column(db.String(20)) # IP Address
    dept = db.relationship('Dept', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, dept, name, position, ip):
        self.dept = dept
        self.user_name = name
        self.user_position = position
        self.user_ip = ip


class AssetHistory(db.Model):
    """
    자산에 대한 정보의 항목 변경에 따른 히스토리 관리 테이블용

    이 테이블에 들어가는 데이터는 asset 객체를 마이너스 연산해서 변경된 데이터만 뽑아낼 수 있어야 한다.
    """
    seq = db.Column(db.Integer, db.Sequence('asset_hist_seq'), primary_key=True)
    asset_code = db.Column(db.String(20)) # 자산코드
    field_name = db.Column(db.String(40)) # 필드명(항목명)
    old_value = db.Column(db.String(255)) # 예전값
    new_value = db.Column(db.String(255)) # 새로운 값
    change_date = db.Column(db.Date) # 변경일자
    change_note = db.Column(db.Text) # 변경사유

    def __init__(self, asset_code, field_name, old_value, new_value):
        self.asset_code = asset_code
        self.field_name = field_name
        self.old_value = old_value
        self.new_value = new_value
        self.change_date = datetime.datetime.now()

    @hybrid_property
    def field_name_display(self):
        field_name_dict = {
            'product_name': u'제품명',
            'config_no': u'Config NO(LG 데스크탑 전용)',
            'send_date': u'지급일',
            'acquire_date': u'취득년월일',
            'acquire_money': u'취득가',
            'disuse_date': u'폐기일',
            'disuse_note': u'폐기사유',
            'make_date': u'제조년월',
            'scan_time': u'최종검사일',
            'os': u'운영체제',
            'service_pack': u'서비스팩',
            'usb_support_type': u'USB 지원 버전',
            'manufacture': u'제조사',
            'product_serial': u'제품번호',
            'processor_version': u'프로세서',
            'memory_size': u'메모리 크기',
            'video_chip': u'비디오칩',
            'hdd_name': u'하드 디스크 모델',
            'hdd_serial': u'하드 디스크 제품번호',
            'hdd_capacity': u'하드 디스크 크기',
            'mac_address': u'Mac Address',
            'windows_version': u'번들 윈도우 버전',
            'windows_serial': u'번들 윈도우 제품번호',
            'netbios_name': u'컴퓨터명(NetBIOS Name)',
            'note': u'비고',
            'collect_date': u'회수일자',
            'user_seq': u'사용자'
        }

        return field_name_dict.get(self.field_name, self.field_name)

    @hybrid_property
    def old_value_display(self):
        # 현재 출력되는 필드가 사용자인 경우 사용자 이름을 출력해줘야 한다.
        if self.field_name == 'user_seq':
            if self.old_value != '':
                return db.session.query(User).filter(User.seq == self.old_value).first().user_name
        return self.old_value

    @hybrid_property
    def new_value_display(self):
        # 현재 출력되는 필드가 사용자인 경우 사용자 이름을 출력해줘야 한다.
        if self.field_name == 'user_seq':
            return db.session.query(User).filter(User.seq == self.new_value).first().user_name
        return self.new_value

"""
class AssetMatchHistory(db.Model):
    seq = db.Column(db.Integer, db.Sequence('asset_match_hist_seq'), primary_key=True)
    user_seq = db.Column(db.Integer, db.ForeignKey('user.seq')) # 유저코드
    asset_code = db.Column(db.String(200), db.ForeignKey('asset.asset_code')) # 자산코드
    send_date = db.Column(db.Date) # 지급일
    collect_date = db.Column(db.Date) # 회수일

    user = db.relationship('User', backref=db.backref('asset_hist', lazy='dynamic'))
    asset = db.relationship('Asset', backref=db.backref('asset_hist', lazy='dynamic'))

    def __init__(self, user, asset, send_date, collect_date):
        self.user = user
        self.asset = asset
        self.send_date = send_date
        self.collect_date = collect_date
"""

class ServiceRequest(db.Model):
    seq = db.Column(db.Integer, db.Sequence('service_request_seq'), primary_key=True)
    receipt_time = db.Column(db.DateTime) # 접수시간
    start_work_time = db.Column(db.DateTime) # 처리시작시간
    end_work_time = db.Column(db.DateTime) # 처리종료시간
    sr_type = db.Column(db.String(100)) # 접수종류(하드웨어, 소프트웨어)
    receipt_note = db.Column(db.Text) # 접수내역
    closed_note = db.Column(db.Text) # 처리내역
    status = db.Column(db.CHAR) # 처리상태(접수, 진행중, 종료)
    user_seq = db.Column(db.Integer) # 접수 신청자 코드
    user_name = db.Column(db.String(20)) # 접수 신청자명
    asset_code = db.Column(db.String(100)) # 어셋코드
