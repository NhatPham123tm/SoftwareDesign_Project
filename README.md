# SoftwareDesign_Project
team_name = Trois-Rivières

# Django Project Setup Guide

## **Prerequisites**
Before running this project, ensure you have the following installed:

- **Python** (3.x)
- **Pipenv** (for virtual environment management)
- **Azure CLI** (for authentication)
- **PostgreSQL** (if running locally, otherwise configure Azure DB)

---

## **🔧 Setup and Run the Project**

### **1️ Activate the Virtual Environment**
Ensure you're in the project directory and run:
```bash
pipenv shell

### **2️⃣ Log in to Azure (Required for DB Connection)**
If you haven’t installed the Azure CLI, install it first:

For Ubuntu (WSL):
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

For Windows:
Download and install from Azure CLI.

Log in to Azure
Run: az login 

If you're using Azure Active Directory authentication for PostgreSQL, you may also need to fetch an access token:
az account get-access-token --resource https://ossrdbms-aad.database.windows.net

### **3️⃣ Run the Django Development Server**

Once logged in, start the Django server:
python manage.py runserver

The server should be accessible at:
http://127.0.0.1:8000/

## *** For accessing database with psql

## 1 Login with run: az login
## 2 bash connection parameter

export PGHOST=troisrivieres.postgres.database.azure.com
export PGUSER=yourUH_EMAIL@CougarNet.UH.EDU
export PGPORT=5432
export PGDATABASE=postgres
export PGPASSWORD="$(az account get-access-token --resource https://ossrdbms-aad.database.windows.net --query accessToken --output tsv)" 

## 3 run psql