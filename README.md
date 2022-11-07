# Tikilord

## Setup

### Pre-requisites

Docker
Docker Compose
Poetry

sudo dnf install poetry
sudo dnf install moby-engine docker-compose
sudo systemctl enable docker
sudo systemctl start docker

## Set Up Secrets

`./secrets/db_name`
`./secrets/db_pass`
`./secrets/db_user`

## Building and Launching

### Build Tikilord Image

sudo docker image build -t tikilord:latest .

### Bring Up Compose Group

sudo docker compose up -d
