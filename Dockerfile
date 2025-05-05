# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the files into the container
COPY . /app/

# Install system dependencies including curl, unzip, and git
RUN apt-get update && \
    apt-get install -y curl unzip git && \
    # Download Allure CLI zip file
    curl -o allure.zip -L https://github.com/allure-framework/allure2/releases/latest/download/allure-2.27.0.zip && \
    # Verify the integrity of the download (optional but recommended)
    unzip allure.zip -d /opt/ && \
    # Create a symlink to make Allure accessible from anywhere
    ln -s /opt/allure-2.27.0/bin/allure /usr/bin/allure && \
    # Clean up
    rm allure.zip && \
    # Upgrade pip and install project dependencies
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Set the default command to run the tests
CMD ["pytest", "--maxfail=2", "--capture=no", "--alluredir=reports/allure-results"]
