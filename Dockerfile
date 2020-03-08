FROM python:3.7-buster

ARG key
ARG iv
ENV key=$key
ENV iv=$iv


ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

# Install Python Requirements
RUN apt-get update -y && apt-get upgrade -y

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn


# Decrypt secrets
WORKDIR $APP_HOME/secrets
RUN openssl aes-256-cbc -K $key -iv $iv -in secrets.tar.enc -out secrets.tar -d && tar xvf secrets.tar

WORKDIR $APP_HOME
# Start securethebox-server service deployed to Google Cloud Run
CMD exec gunicorn --bind :$PORT --workers 1 --threads 3 main:app