===== 
Proper: Small CMS for BIZ
===== 
simple service
-------- 

�ϵ���� �ڻ���� ���α׷��Դϴ�.

��ġ���

1. VirtualEnv ȯ�汸��

$ easy_install virtualenv

$ virtualenv venv

2. ���̺귯�� ��ġ

$ source venv/bin/activate
(venv)$ easy_install flask==0.10.1 jinja2==2.7.1 markupsafe==0.18 sqlalchemy==0.9.1 webhelpers==1.3 tornado==3.2 flask-sqlalchemy==1.0 python-dateutil

3. �����ͺ��̽� ����

���� �����ͺ��̽� : PostgreSQL 9.1

���� �����ͺ��̽� �� ����� :

  - �����ͺ��̽� : proper
  
  - ����� : proper
  
  - ��й�ȣ : 1234


3. ���α׷� ����

$ python serv_start.py

4. ����

http://localhost/pc


:Authors: 
    Jiho Lee, 
    Haibane
    This is Test Version

:Version: 1.0 of 2013/12/24 
