# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the files into the container
COPY . /app/

# Install system and Python dependencies including Allure CLI
RUN apt-get update && \
    apt-get install -y curl unzip git && \
    curl -o allure.zip -L https://github.com/allure-framework/allure2/releases/latest/download/allure-2.27.0.zip && \
    unzip allure.zip -d /opt/ && \
    ln -s /opt/allure-2.27.0/bin/allure /usr/bin/allure && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Set the default command to run the tests
CMD ["pytest", "--maxfail=2", "--capture=no", "--alluredir=reports/allure-results"]
