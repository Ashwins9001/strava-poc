### Overview 

Just a simple project to fetch data from Strava and show some analytics on it using Airflow, PySpark and Docker to automate construction/destruction of the app and to learn to orchestrate tasks using DAGs.

### Docker-Compose
Spin up Postgres DB, Airflow webserver and scheduler separately. 

By default creates an 'admin' user to connect to the Airflow landing page hosted on localhost:8080. Refresh the cache or run in incognito mode to access once started.

Postgres DB is made to store Airflow metadata such as logging information.

1. Run docker-compose up --build
2. Open incognito tab to: localhost:8080, sign in to AirFlow environment