# SoftwareDesign_Project
team_name = Trois-Rivières

# Django Project Setup Guide

## 1. Prerequisites
Before downloading and running this project, ensure you have the following installed:

- **Python** (3.x)
- **PostgreSQL** 


## 2. 🔧 Setup and Run the Project
- pip install -r requirements.txt    for Windows
- pip3 install -r requirements.txt    for macOS

## 3. Create your local PostgreSQL database

## 4. Connect PosgreSQl to app
Create .env file in the main directory with the following info connection:
- DB_NAME= #DB name my_db         
- DB_USER= postgres #DB user, default = postgres
- DB_PASSWORD= #DB password
- DB_HOST=localhost #DB host, default = localhost
- DB_PORT=5432 #DB port, default = 5432

## 5. Apply makemigrations and migration to initialize database with initial data
Windows:
- python manage.py makemigrations
- python manage.py migrate

macOS:
- python3 manage.py makemigrations
- python3 manage.py migrate

Note: If no initialized data is in the database rerun the above commands.

## 6. Server/ Web Deployment
- python manage.py runserver    (Window)
- python3 manage.py runserver   (MacOs)

## 7. Web location
http://localhost:8000/

## 8. Create and Login an account
No account or no Microsoft account is linked to our account.

=> Register a new account manually or link with a Microsoft account (Both need a User ID - 7 digits)
- Note: Currently any unique 7-digits are acceptable since we have no provided User-ID list to bound.

Login by email or Microsoft Authorization


