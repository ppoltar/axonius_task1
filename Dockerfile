# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the files into the container
COPY . /app/

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl unzip git && \
    curl -v -L https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.27.0/allure-commandline-2.27.0.zip -o allure.zip && \
    unzip -t allure.zip && \
    unzip -o allure.zip -d /opt/ && \
    ls -la /opt && \
    mv /opt/allure-2.27.0 /opt/allure && \
    ln -s /opt/allure/bin/allure /usr/local/bin/allure && \
    rm allure.zip

# Set the default command to run the tests
CMD ["pytest", "--maxfail=2", "--capture=no", "--alluredir=reports/allure-results"]
