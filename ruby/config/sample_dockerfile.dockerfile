FROM alpine:latest
LABEL authors="pradeep@seleniumframework.com"

RUN apk update && \
    apk upgrade && \
    apk add git