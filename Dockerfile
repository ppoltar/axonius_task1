FROM openjdk:11-jre-slim

# Install Python, pip, curl, unzip, git, etc.
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    unzip \
    git && \
    apt-get clean

# Install Playwright dependencies
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install playwright && \
    python3 -m playwright install-deps && \
    python3 -m playwright install

# Install Allure Command Line
RUN curl -v -L https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.27.0/allure-commandline-2.27.0.zip -o allure.zip && \
    unzip allure.zip -d /opt/ && \
    rm allure.zip && \
    ln -s /opt/allure-2.27.0/bin/allure /usr/local/bin/allure

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Set the default command to run tests
CMD ["pytest", "--maxfail=2", "--capture=no", "--alluredir=reports/allure-results"]
