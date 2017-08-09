Application setup:

1) Ensure python3.4-dev, virtualenv and postgresql-server-dev-9.4 are installed

2) virtualenv -p /usr/bin/python3.4 venv3.4

3) source venv3.4/bin/activate

4) pip install -r requirements.txt

5) Enter correct machine ip in config.py

6) sudo su - postgres
    
    a) create user service-registry_user with password 'apj0702';
    
    b) create database service-registry_database with owner service-registry_user;

7) python shell

    a) from controller import application
    
    b) from models import db
    
    c) db.create_all()