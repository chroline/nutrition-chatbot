# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9.16

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the download_model.py script to generate additional files
RUN python util/download_model.py

# Expose the port that the FastAPI application will be listening on
EXPOSE $PORT

# Set the command to run the FastAPI application using Uvicorn
CMD uvicorn server:app --host 0.0.0.0 --port $PORT