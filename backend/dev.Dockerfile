FROM python:3.8-slim

RUN mkdir -p /usr/src/app
RUN mkdir -p /usr/src/app/backend

WORKDIR /usr/src/app/backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP_PORT=$FLASK_APP_PORT
ENV FLASK_APP_FRONTEND=$FLASK_APP_FRONTEND
ENV FLASK_APP_PROXY=$FLASK_APP_PROXY
ENV FLASK_APP_PROD=$FLASK_APP_PROD
ENV FLASK_APP_HOST_IP=$FLASK_APP_HOST_IP
ENV FLASK_APP_HOST_NAME=$FLASK_APP_HOST_NAME
EXPOSE $FLASK_APP_PORT

CMD ["python", "app.py"]

