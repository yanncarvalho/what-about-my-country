# ![What about my country](../images/application-title.png "Application logo") __Frontend__ #

![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=for-the-badge&logo=vuedotjs&logoColor=%234FC08D)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)
![Chart.js](https://img.shields.io/badge/chart.js-F5788D.svg?style=for-the-badge&logo=chart.js&logoColor=white)
![Cypress](https://img.shields.io/badge/-cypress-%23E5E5E5?style=for-the-badge&logo=cypress&logoColor=058a5e)
![GraphQL](https://img.shields.io/badge/-GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

This vue frontend application provides information and charts about countries, consuming this information from a GraphQL request.

[Read more about backend](../backend/README.md "Read more about backend").

## How to run ##

### Using docker image ###

It can be run the project's docker image by the instruction:

``` sh
docker run -p [port]:80 --env BACKEND_ADDRESS=[backend address] --env BACKEND_PORT=[backend port] yanncarvalho/wbmc-frontend:latest 
```

### Run without docker container ###

To run the application without docker, it is necessary to inform values ​​for parameters in the .env, and then run the command:

``` sh
npx vite
```

## Compile project ##

To compile the project run the command:

``` sh
npm run build
```

## Acess JsDoc ##

To access the JsDoc reference for this application, run the command:

``` sh
npx jsdoc -r -c ./.jsdoc.conf.json
```

## Author ##

Made by [Yann Carvalho](https://www.linkedin.com/in/yann-carvalho-764abab6/).

## Licensing ##

What about my country is licensed under the Apache 2.0 License. See [LICENSE](../LICENSE) for the full license text.
