# Use python-3 base image
FROM python:3

# Setup the Working Directory
WORKDIR /iotblockchainApp

# Copy the configuration file (if not copied)
COPY production.cfg /iotblockchainApp

# Add all files to the Working Directory
ADD . /iotblockchainApp

# Install Dependencies for app
RUN pip install -r requirements.txt

# Set configuration file as environment variable
ENV FLASK_APP app.py

EXPOSE 5000

CMD ["uwsgi", "--ini", "app.ini"]