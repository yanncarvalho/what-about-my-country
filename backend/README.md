# ![What about my country](../images/application-title.png "Application logo") __Backend__ #

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![GraphQL](https://img.shields.io/badge/-GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

This backend Django application provides information from the [World Bank database](https://databank.worldbank.org/) exposing with GraphQL.

[Read more about frontend](../frontend/README.md "Read more about frontend").

## How to run ##

### Using docker image ###

It can be run the project's docker image by the instruction:

``` sh
docker run -p [port]:80 --env REDIS_HOST=[redis address] --env REDIS_PORT=[redis port] yanncarvalho/wbmc-backend:latest
```

### Run without docker container ###

To run the application without docker, it is necessary to inform which profile will be executed using the APP_ENVIRONMENT environment variable (by default its value is development _dev_), furthermore it need be informed values ​​for parameters in the ./envs directory:

``` sh
export APP_ENVIRONMENT=[dev|prod] &&
python3 -m venv venv &&
source venv/bin/activate &&
pip install --upgrade pip &&
pip install -r requirements.txt &&
python3 manage.py runserver
```

## Additional information ##

When sending the first request, the redis is populated, although it is also possible to populate using the command:
  
``` sh
python3 manage.py populate_redis
```

## Author ##

Made by [Yann Carvalho](https://www.linkedin.com/in/yann-carvalho-764abab6/).

## Licensing ##

What about my country is licensed under the Apache 2.0 License. See [LICENSE](../LICENSE) for the full license text.
