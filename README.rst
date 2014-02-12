===== 
Proper: Small CMS for BIZ
===== 
simple service
-------- 

하드웨어 자산관리 프로그램입니다.

설치방법

1. VirtualEnv 환경구성

$ easy_install virtualenv

$ virtualenv venv

2. 라이브러리 설치

$ source venv/bin/activate
(venv)$ easy_install flask==0.10.1 jinja2==2.7.1 markupsafe==0.18 sqlalchemy==0.9.1 webhelpers==1.3 tornado==3.2 flask-sqlalchemy==1.0 python-dateutil

3. 데이터베이스 구성

지원 데이터베이스 : PostgreSQL 9.1

생성 데이터베이스 및 사용자 :

  - 데이터베이스 : proper
  
  - 사용자 : proper
  
  - 비밀번호 : 1234


3. 프로그램 실행

$ python serv_start.py

4. 접속

http://localhost/pc


:Authors: 
    Jiho Lee, 
    Haibane
    This is Test Version

:Version: 1.0 of 2013/12/24 
