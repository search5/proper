#-*- coding: utf-8 -*-
import math
import datetime
import os.path

def paging_env_calc(perPage, currPage, totalCnt):
    total_page = int(math.ceil(float(totalCnt) / float(perPage)))

    # 목록을 가져올 시점 계산
    limitStart = perPage * (int(currPage) - 1)

    # 이전, 다음 페이지 번호 계산
    prev_page_number = currPage - 1
    if prev_page_number < 1:
        # 이전 페이지 번호가 1보다 작으면 1로 이전 페이지 번호를 설정한다.
        prev_page_number = 1

    next_page_number = currPage + 1
    if next_page_number > total_page:
        # 다음 페이지 번호가 전체 페이지 보다 크면 전체 페이지를 다음 페이지 수로 설정한다.
        next_page_number = total_page

    return dict(totalPage=total_page, limitStart=limitStart, prevPageNum=prev_page_number, nextPageNum=next_page_number)

def generateTimeBaseFileName(orginal_file_name):
    nowMicrotime = datetime.datetime.now()
    newFileNameExcludeExtension = nowMicrotime.strftime('%Y%m%d%H%M%S%f')
    
    orgFileNameInfo = os.path.splitext(orginal_file_name)
    
    return str(newFileNameExcludeExtension) + orgFileNameInfo[1]