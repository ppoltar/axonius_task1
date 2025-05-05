# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install system dependencies for Playwright, Allure, and OpenJDK 11
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    git \
    openjdk-11-jdk \
    libnss3 \
    libatk1.0-0 \
    libcups2 \
    libx11-xcb1 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libxss1 \
    libasound2 \
    libx11-6 \
    fonts-liberation \
    libappindicator3-1 \
    libxtst6 \
    xdg-utils \
    && apt-get clean  # Clean up after installation

# Set JAVA_HOME and update PATH for OpenJDK 11
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt /app/

# Install Python dependencies and Playwright dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    # Install Playwright and its required dependencies
    python -m playwright install-deps && \
    python -m playwright install

# Install Allure Commandline (a Java-based tool)
RUN curl -v -L https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.27.0/allure-commandline-2.27.0.zip -o allure.zip && \
    unzip -t allure.zip && \
    unzip -o allure.zip -d /opt/ && \
    ls -la /opt && \
    mv /opt/allure-2.27.0 /opt/allure && \
    ln -s /opt/allure/bin/allure /usr/local/bin/allure && \
    rm allure.zip

# Copy the rest of the application files into the container
COPY . /app/

# Set the default command to run the tests
CMD ["pytest", "--maxfail=2", "--capture=no", "--alluredir=reports/allure-results"]
