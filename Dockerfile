# We will use python:3.10-alpine as the base image for building the Flask container
FROM python:3.10-alpine

# It specifies the working directory where the Docker container will run
WORKDIR /app

# Copying all the application files to the working directory
COPY .. .

# Change directory to the location of our newly copied python codebase
WORKDIR /app/python

# Install all the dependencies required to run the Flask application
RUN pip install -r requirements.txt

# Run the application using gunicorn with 8 workers at port 1911
CMD ["gunicorn", "-w", "8", "-b", "0.0.0.0:1911", "wsgi:flask_api"]