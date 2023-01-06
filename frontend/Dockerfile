# Base
FROM node:19-alpine as base-stage
COPY . .
RUN npm install

# Build
FROM node:19-alpine as build-stage
ARG BACKEND_ADDRESS
ARG BACKEND_PORT
COPY --from=base-stage . .
RUN npm run build

# Production
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /dist /usr/share/nginx/html
COPY ./docker/entrypoint.sh .
EXPOSE 80
ENTRYPOINT [ "sh", "entrypoint.sh" ]
