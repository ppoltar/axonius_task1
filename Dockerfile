# Use an OpenJDK 11 base image
FROM openjdk:11-jre-slim

# Install Python, pip, curl, unzip, git, and required system libraries for Playwright
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    unzip \
    git \
    libnss3 \
    libatk1.0-0 \
    libcups2 \
    libx11-xcb1 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libxss1 \
    libasound2 \
    libx11-6 && \
    apt-get clean  # Clean up after package installation to reduce image size

# Install Playwright and its dependencies
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install playwright && \
    python3 -m playwright install-deps && \
    python3 -m playwright install  # Downloads and installs the necessary browser binaries (Chromium, WebKit, Firefox)

# Install Allure Command Line tool
RUN curl -v -L https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.27.0/allure-commandline-2.27.0.zip -o allure.zip && \
    unzip allure.zip -d /opt/ && \
    rm allure.zip && \
    ln -s /opt/allure-2.27.0/bin/allure /usr/local/bin/allure  # Creates a symlink for easier access to the allure command

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies specified in requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Set the default command to run tests using pytest
CMD ["pytest", "--maxfail=2", "--capture=no", "--alluredir=reports/allure-results"]
