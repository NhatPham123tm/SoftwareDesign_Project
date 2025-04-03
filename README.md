# SoftwareDesign_Project
team_name = Trois-Rivières

# Local Django Project Setup Guide
## Prerequisites
Before downloading and running this project, ensure you have the following installed:

- **Python** (3.x)
- **PostgreSQL** 
- **Docker Desktop**
- **Full Feature PDF reader (Recommend: Adobe Reader) or open PDF with Firefox**

NOTE: To view the fully functional PDF with the checked box, please use a Full-Feature PDF reader (Recommend: Adobe Reader) or Firefox browser.

### Using Docker To Run Project
Follow these steps to set up and run the application and database.

## 1. Setup Docker on Your Machine

Ensure that you have Docker and Docker Compose installed. Refer to `./docker-setup.md` for more details.

## 2. Set Environment Variables

Before running the application, you need to set up environment variables. These are defined in the `.env` file located in the root of your repository. Below is a summary of the variables you need to configure:

| Variable          | Description                        | Default Value |
|-------------------|------------------------------------|---------------|
| DB_USER     | PostgreSQL database username       | trois        |
| DB_PASSWORD | PostgreSQL database password       | abc           |
| DB_NAME       | Name of the PostgreSQL database    | trois-rivieres    |
| POSTGRES_PORT     | Port for PostgreSQL database       | 5432          |
| APP_PORT          | Port for the application           | 8000          |
| DB_HOST      | Host in Docker container   | db |
| DEBUG      | debug option   | True |
| DJANGO_LOGLEVEL      | log option   | info |
| DJANGO_ALLOWED_HOSTS      | host option   | "" |
| DB_ENGINE     | engine option   | "django.db.backends.postgresql" |
| MICROSOFT_AUTH_CLIENT_ID     | outlook login requirement   | check download file or contact team member |
| MICROSOFT_AUTH_CLIENT_SECRET     | outlook login requirement   | check download file or contact team member |
| MICROSOFT_AUTH_TENANT_ID     | outlook login requirement   | check download file or contact team member |
| MICROSOFT_AUTH_REDIRECT_URI     | outlook login requirement   | check download file or contact team member |
| SECRET_KEY     | django db key   | check download file or contact team member |

Note: data in Azure is not filled due to GitHub security, but you can download .env file here: https://drive.google.com/file/d/1mbCinPit1p-oDe-14SRV8TOyRTRwQMtN/view?usp=sharing 

**NOTE:Postgres User and Database will be created based on the variables set, no prior setup is needed**
Ensure that these variables are correctly set in your `.env` file.

## 3. Start Up the App and Database

For first time running:
```
chmod +x entrypoint.sh
docker-compose up --build
```
This gonna take a while

After that, whenever to start the app and database containers run :

```
docker-compose up
```

If you change dependencies during development, you'll need to rebuild the Docker image to install the new dependencies inside the container:

```
docker-compose up --build
```

### Access the Application

#### **To access webpage:**
Open your browser and navigate to `http://localhost:{APP_PORT}` to access the application.

#### **To access the postgres db terminal:**

find the name of the container running the **database**:
```
docker ps -a
```
~copy the name of the image running `postgres:13` 


```
docker exec -it {db-container-name} psql -U {POSTGRES_USER} -d {POSTGRES_DB}
```

#### **To access the application terminal:**

~find the name of the container running the **application**:
```
docker ps -a
```

during development if you change code you don't need to stop the containers, it will auto reload!
~copy the name of the image running the **app** 


```
docker exec -it {app-container-name} sh
```

### Stopping and Removing Containers and Volumes

To stop the containers and remove the associated volumes (this will delete the database data), run:
```
docker-compose down --volumes
```

This command stops the containers and removes the volumes, effectively deleting the database data.

If you just want to stop the containers but keep the data in them, run:

```
docker-compose down
```

### Run using django only

## 1. 🔧 Setup and Run the Project
- pip install -r requirements.txt    for Windows
- pip3 install -r requirements.txt    for macOS
- apt-get install -y texlive-latex-base texlive-fonts-recommended texlive-fonts-extra
## 2. Create your local PostgreSQL database

## 3. Connect PosgreSQl to app
Create .env file in the main directory with the following info connection:
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

Note: data in Azure is not filled due to GitHub security, but you can download .env file here: https://drive.google.com/file/d/1Ur6PS5JKRTOn3OWM0o7Dg-NkggFfO37O/view?usp=sharing 

## 4. Apply makemigrations and migration to initialize database with initial data
Windows:
- python manage.py makemigrations
- python manage.py migrate

macOS:
- python3 manage.py makemigrations
- python3 manage.py migrate

Note: If no initialized data is in the database rerun the above commands.

## 5. Server/ Web Deployment
- python manage.py runserver    (Window)
- python3 manage.py runserver   (MacOs)

## 6. Web location
http://localhost:8000/

## 7. Create and Login an account
No account or no Microsoft account is linked to our account.

=> Register a new account manually or link with a Microsoft account (Both need a User ID - 7 digits)
- Note: Currently any unique 7-digits are acceptable since we have no provided User-ID list to bound.

Login by email or Microsoft Authorization

Testing accounts:
- admin@example.com/admin123
- user@example.com/user123

Note: Use the Log Out button for the best experience after each access. If any page is not loading properly, try clearing cookies and local storage using the browser's developer tools.

# Online Deployment:
## https://trois-user-management-cuaed0fhgch5hza9.centralus-01.azurewebsites.net/
Login your Cougarnet Account in browser before directing app location (avoid Microsoft blocking)

You can create a new account or login with Testing accounts:
- admin@example.com/admin123
- user@example.com/user123
