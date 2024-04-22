FROM python:3.9.9-alpine
WORKDIR /api
COPY . ./app/

RUN apk add --update --no-cache bash curl ca-certificates openssl \
    && adduser -S api -u 1111  \
    && pip3 install -r ./app/requirements.txt

ENV SERVE_PORT="8080"
ENV SECRET_KEY="dev"
ENV FLASK_APP="app"
ENV FLASK_ENV="production"

RUN flask init-db \
    && chown 1111:1111 -R ./instance

ENTRYPOINT ["waitress-serve"]