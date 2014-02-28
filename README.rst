========================= 
Proper: Small CMS for BIZ
========================= 
------------
simple service
------------

하드웨어 자산관리 프로그램입니다.

=======
설치방법
=======

1. VirtualEnv 환경구성

    $ easy_install virtualenv
    $ virtualenv venv
    

2. 라이브러리 설치

    virtualenv        
        $ source venv/bin/activate
        (venv)$ easy_install flask==0.10.1 jinja2==2.7.1 markupsafe==0.18 sqlalchemy==0.9.1 webhelpers==1.3 tornado==3.2 flask-sqlalchemy==1.0 python-dateutil psycopg2
        
    윈도우 환경에서 구축시에는 psycopg2 모듈이 별도로 설치되어야 가능합니다.


    ubuntu + pip + virtualenvwrapper 이용시.
    
        $ sudo pip install virtualenvwrapper
        $ vi ~{user}/.bashrc 수정        
            export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/pythonexport        
            VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenvsource        
            /usr/local/bin/virtualenvwrapper.sh
        
        
        $ source ~{user}/.bashrc        
        $ mkvirtualenv --distribute --no-site-packages [virtualenv name] --python=[python path]``
        $ sudo apt-get install libpq-dev python-dev : psycopg2 를 pip 설치시 미리 있어야 하는 패키지.``
        $ (virtualenv name) pip install -r requirement.txt``


3. 데이터베이스 구성

    지원 데이터베이스 : PostgreSQL 9.1
    
    생성 데이터베이스 및 사용자 :
        - 데이터베이스 : proper
        - 사용자 : proper
        - 비밀번호 : 1234


    (venv)$ python
        >>> from proper import db        
        >>> db.create_all()

        

4. 프로그램 실행
    
    $ python serv_start.py



5. 접속

    http://localhost/pc



:Authors: 
    Jiho Lee, 
    Haibane
    This is Test Version

:Version: 1.0.1 of 2014/02/17 