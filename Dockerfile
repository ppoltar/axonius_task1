# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the files into the container
COPY . /app/

# Install system dependencies including curl, unzip, and git
RUN apt-get update && \
    apt-get install -y curl unzip git && \
    # Download Allure CLI from Maven Central
    curl -L https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.27.0/allure-commandline-2.27.0.zip -o allure.zip && \
    # Unzip the Allure CLI and create symlink
    unzip allure.zip -d /opt/ && \
    ln -s /opt/allure-commandline-2.27.0/bin/allure /usr/bin/allure && \
    # Clean up by removing the zip file
    rm allure.zip && \
    # Upgrade pip and install project dependencies
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Set the default command to run the tests
CMD ["pytest", "--maxfail=2", "--capture=no", "--alluredir=reports/allure-results"]
