### Overview 

Just a simple project to fetch data from Strava and show some analytics on it using Airflow, PySpark and Docker to automate construction/destruction of the app and to learn to orchestrate tasks using DAGs.

### Docker-Compose
Spin up Postgres DB, Airflow webserver and scheduler separately. 

By default creates an 'admin' user to connect to the Airflow landing page hosted on localhost:8080. Refresh the cache or run in incognito mode to access once started.

Postgres DB is made to store Airflow metadata such as logging information.

1. Run docker-compose up --build
2. Open incognito tab to: localhost:8080, sign in to AirFlow environment

### Getting Strava Connected
Note: I'll add arguments to do things programatically later, for now authentication is a bit manual.

1. Run test_strava.py and this function in it specifically: authenticate_to_read_all_scope to fetch Strava scope for your account.
2. Go to outputted URL, sign in to your personal Strava account, and fetch the authentication token from redirect URL (its the section that comes after 'code'). 
3. Update AUTHENTICATION_CODE env variable with the redirect URL's provided code.
4. Run test_strava.py again and this function in it specifically: initialize_responses. This will update the strava_leaflet_map.html file!

### Mapped Out Routes
All routes are separated into segments by Haversine distance formula. Hence any two coordinates exceeding a distance of 8KM are seperated to distinct segments, we use this to draw things out since leaflet can draw lists of coordinate-pairs in layers by color.
![Map Preview](images/map_preview.png)