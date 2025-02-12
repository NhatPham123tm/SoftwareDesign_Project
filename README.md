# SoftwareDesign_Project
team_name = Trois-Rivières

# Django Project Setup Guide

## **Prerequisites**
Before running this project, ensure you have the following installed:

- **Python** (3.x)
- **PostgreSQL** 

---

## **🔧 Setup and Run the Project**

### **1️ Create your local postgreSQL database **

### **2 change database connection parameters and add authentication key in UserManagement/setting.py**
contact me for key

## ***3 Install all dependencies
pip install -r requirements.txt

## ***4 Apply migration
python manage.py makemigrations
python manage.py migrate

or 
python3 manage.py makemigrations
python3 manage.py migrate

## ***5 run server
python manage.py runserver
or
python3 manage.py runserver

## ***6 go to your browser
http://127.0.0.1:8000/

goto login -> login with Microsoft