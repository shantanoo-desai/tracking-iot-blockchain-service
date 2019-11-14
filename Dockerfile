# Use python-3 base image
FROM python:3

LABEL maintainer="Shan Desai<shantanoo.desai@gmail.com>"

# Setup the Working Directory
WORKDIR /iotblockchainApp

# Add all files to the Working Directory
ADD . /iotblockchainApp

# Install Dependencies for app
RUN pip install -r requirements.txt

# Set configuration file as environment variable
ENV FLASK_APP app.py

CMD ["uwsgi", "--ini", "app.ini"]