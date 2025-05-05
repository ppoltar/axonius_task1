FROM python:3.11-bullseye

# Install required system dependencies for Playwright, Allure, and OpenJDK 11
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    git \
    wget \
    ca-certificates \
    software-properties-common \
    && apt-get clean

# Add OpenJDK repository and install OpenJDK 11
RUN echo "deb http://deb.debian.org/debian/ bookworm-backports main" | tee -a /etc/apt/sources.list.d/debian-backports.list && \
    apt-get update && \
    apt-get install -y openjdk-11-jdk

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
