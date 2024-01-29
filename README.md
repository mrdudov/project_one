# Project ONE

## Build instruction

* clone repository

      git clone git@github.com:mrdudov/project_one.git

* get into project directory

      cd ./project_one

* rename .env_empty в .env

      mv ./backend/.env_empty ./backend/.env

* build containers

      docker-compose up --build -d

* make migrations

      docker-compose exec web alembic upgrade head

* open open api documentation page

      http://localhost:8080/docs#/

## Commands

    docker compose exec api alembic revision --autogenerate -m "init"

    docker compose exec api alembic upgrade head

## Create a random secret key

To generate a secure random secret key use the command:

    openssl rand -hex 32
    09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
