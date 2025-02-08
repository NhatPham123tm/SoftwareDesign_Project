# SoftwareDesign_Project
team_name="Trois-Rivières"

# Django Project Setup Guide

## Prerequisites
# Before running this project, ensure you have the following installed:
Make sure you have installed:
1. Python (3.x)
2. Pipenv (for virtual environment management)
3. Azure CLI (for authentication)
4. PostgreSQL (if running locally, otherwise configure Azure DB)

# Setup and Run the Project

## Step 1: Activate the Virtual Environment
pipenv shell

## Step 2: Log in to Azure (Required for DB Connection)
run:
az login

# If using Azure Active Directory authentication for PostgreSQL:
run:
az account get-access-token --resource https://ossrdbms-aad.database.windows.net

## Step 3: Run the Django Development Server
python manage.py runserver
or
python3 manage.py runserver

# If accessing the Database with psql

# Step 1: Login to Azure
az login

# Step 2: Export environment variables for PostgreSQL connection
export PGHOST=troisrivieres.postgres.database.azure.com

export PGUSER=yourUH_EMAIL@CougarNet.UH.EDU

export PGPORT=5432

export PGDATABASE=postgres

export PGPASSWORD="$(az account get-access-token --resource https://ossrdbms-aad.database.windows.net --query accessToken --output tsv)" 

# Step 3: Run PostgreSQL client
psql
