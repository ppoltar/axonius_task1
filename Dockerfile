# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the files into the container
COPY . /app/

# Install system dependencies and Python dependencies
RUN apt-get update && \
    apt-get install -y \
    curl \
    git \
    && pip install --upgrade pip && \
    pip install -r requirements.txt

# Set the default command to run the tests
CMD ["pytest", "--maxfail=2", "--capture=no", "--alluredir=reports/allure-results"]
