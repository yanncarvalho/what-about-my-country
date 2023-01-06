# Base
FROM python:3.10-alpine as base-stage
RUN pip install --upgrade pip
COPY ./requirements.txt requirements.txt
RUN  pip install -r requirements.txt

# Production
FROM python:3.10-alpine as production
ARG BACKEND_PORT=8080
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY --from=base-stage /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=base-stage /usr/local/bin/ /usr/local/bin/
COPY . /app
EXPOSE $BACKEND_PORT
ENTRYPOINT ["python3"]
CMD ["/app/manage.py", "runserver"]
