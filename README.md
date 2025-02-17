# SoftwareDesign_Project
team_name = Trois-Rivières

# Django Project Setup Guide

## **Prerequisites**
Before running this project, ensure you have the following installed:

- **Python** (3.x)
- **PostgreSQL** 

---

## **🔧 Setup and Run the Project**
Run "pip install -r requirements.txt" for Windows

### **1 Create your local empty PostgreSQL database **

## ***2 Connect PosgreSQl to app
Create .env file in main directory with following info connection:
- DB_NAME= #DB name my_db         
- DB_USER= postgres #DB user, default = postgres
- DB_PASSWORD= #DB password
- DB_HOST=localhost #DB host, default = localhost
- DB_PORT=5432 #DB port, default = 5432
- MICROSOFT_AUTH_CLIENT_ID = ""
- MICROSOFT_AUTH_CLIENT_SECRET = "" 
- MICROSOFT_AUTH_TENANT_ID = ""
- MICROSOFT_AUTH_REDIRECT_URI = ""
- SECRET_KEY = ''

## ***5 Apply migration
Windows:
python manage.py makemigrations
python manage.py migrate

or MacOs:
python3 manage.py makemigrations
python3 manage.py migrate

## ***6 Use Query tools to run the populate_users.sql script under db_script for initializing the first data.

## ***7 run server
python manage.py runserver
or
python3 manage.py runserver

## ***8 go to your browser
http://127.0.0.1:8000/

goto login -> login with Microsoft
