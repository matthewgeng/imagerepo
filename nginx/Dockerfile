FROM nginx:stable-alpine

WORKDIR /nginx
COPY . /nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf.template /etc/nginx/templates/default.conf.template 
# COPY nginx.conf-test.template /etc/nginx/nginx.conf

RUN apk update && \
    apk add openssl && \
    chmod 700 /etc/ssl/private && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt -subj "/C=CA/ST=STATE/L=CITY/O=ORG/OU=DEPARTMENT/CN=localhost" && \
    openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
