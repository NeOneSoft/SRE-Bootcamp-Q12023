# Running the Application in a Docker Container
Prerequisites:
- Docker installed on your system
- Access to the public image repository on DockerHub (in this case neonesoft/wize-gonzalo-romero:latest)

Steps

1.- Pull the public image from DockerHub using the following command:

            docker pull neonesoft/wize-gonzalo-romero:latest

2.' Run the container using the following command:

        docker run -p 8000:8000 neonesoft/wize-gonzalo-romero:latest


This will start a container and map port 8000 on the host to port 8000 in the container. The application will be accessible at http://localhost:8000 in the host's web browser.

Commands for test purposes

```
curl -d "username=admin&password=15e24a16abfc4eef5faeb806e903f78b188c30e4984a03be4c243312f198d1229ae8759e98993464cf713e3683e891fb3f04fbda9cc40f20a07a58ff4bb00788" http://localhost:8000/login

{
  "data":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.StuYX978pQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI"
}
```

```
curl -H 'Accept: application/json' -H "Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4ifQ.StuYX978pQGnCeeaj2E1yBYwQvZIodyDTCJWXdsxBGI" localhost:8000/protected

{
  "data": "You are under protected data"
}
```

Running locally:

Prerequisites:

1.- Set the following environment variables:

- DB_HOST
- DB_USER
- DB_PASSWORD
- DB_NAME
- DB_PORT
- SECRET_KEY
- ADMIN_PASSWORD
- NOADMIN_PASSWORD
- BOB_PASSWORD
- ADMIN_TOKEN

Those values are provided in the README.md or stored in database.

2.- Creat a Python 3 virtual env

```
python3 -m venv env
```

3.- Activate the virtual env

```
source env/bin/activate
```

4.- Install dependencies

```
pip install -r requirements.txt
```

5.- Run the application

```
python3 api.py
```

Running tests

While api.py is running, open a new terminal and execute:

```
python3 tests.py
```
