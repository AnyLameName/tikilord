# Tikilord

## Setup

### Pre-requisites
This is assuming you are using Fedora. Substitute as appropriate for your distribution.   
```
sudo dnf install poetry  
sudo dnf install npm
sudo dnf install moby-engine docker-compose  
sudo dnf install python3-psycopg2 libpq-devel
sudo systemctl enable docker  
sudo systemctl start docker

```
## Set Up Secrets
Create a secrets directory in the top level of the repository, with the following three files. Fill them in as appropriate for your database.

secrets/db_name  
secrets/db_user  
secrets/db_pass  

## SELinux

SELinux interferes with docker's ability to read secrets. This is likely fixable but while we are still in not-ready-for-production mode, the easiest option is Permissive mode.

## Building and Launching

### Build Tikilord Image

```
sudo docker image build -t tikilord:latest .
cd tikiweb
sudo docker image build -t tikweb:latest .
cd ..
sudo docker-compose up -d
```

### Prepare Database

At this point, http://localhost:3000/ on the docker host should get you a broken-looking website, which tells us that the `web` service is up and running. Now we need to initialize the `db` service's database, so it can stop throwing errors when data is requested.

sudo docker-compose run django sh -c "poetry run python manage.py migrate"
