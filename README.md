# ![What about my country](./images/application-title.png "Application logo") #

![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)
![GraphQL](https://img.shields.io/badge/-GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

[![Tests](https://github.com/yanncarvalho/what-about-my-country/actions/workflows/tests.yml/badge.svg)](https://github.com/yanncarvalho/what-about-my-country/actions/workflows/tests.yml)
[![Docker push](https://github.com/yanncarvalho/what-about-my-country/actions/workflows/docker.yml/badge.svg?branch=main)](https://github.com/yanncarvalho/what-about-my-country/actions/workflows/docker.yml)

A web application that provides information about different countries from the [World Bank database](https://databank.worldbank.org/) and create charts.

## Built with ##

- Python 3.10
- Django 4.1
- Redis 7.0.7
- Vue 3.2
- Bootstrap 5.2
- Cypress 12.2.0

## How to run ##

### Using docker compose ###

To run the application with docker compose run the command:

``` sh
export BACKEND_SECRET_KEY=[key] &&
docker compose --env-file .env up
```

### Using docker image ###

It can be downloaded the project's docker images by the instructions:

#### Backend ####

``` sh
docker run -p [port]:80 --env REDIS_HOST=[redis address] --env REDIS_PORT=[redis port] yanncarvalho/wbmc-backend:latest
```

#### Frontend ####

``` sh
docker run -p [port]:80 --env BACKEND_ADDRESS=[backend address] --env BACKEND_PORT=[backend port] yanncarvalho/wbmc-frontend:latest 
```

### Run without docker container ###

To run without docker container [see backend readme](./backend/README.md "See backend readme") and [see frontend readme](./frontend/README.md "See frontend readme").

## Author ##

Made by [Yann Carvalho](https://www.linkedin.com/in/yann-carvalho-764abab6/).

## Licensing ##

What about my country is licensed under the Apache 2.0 License. See [LICENSE](LICENSE) for the full license text.
