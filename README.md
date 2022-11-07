# Tikilord

## Setup

### Pre-requisites
This is assuming you are using Fedora. Substitute as appropriate for your distribution.   
```
sudo dnf install poetry  
sudo dnf install moby-engine docker-compose  
sudo systemctl enable docker  
sudo systemctl start docker

sudo dnf install npm
cd tikiweb/
npm install
```
## Set Up Secrets
Create a secrets directory in the top level of the repository, with the following three files. Fill them in as appropriate for your database.

secrets/db_name  
secrets/db_user  
secrets/db_pass  

## Building and Launching

### Build Tikilord Image

`sudo docker image build -t tikilord:latest .`

### Bring Up Compose Group

`sudo docker compose up -d`
