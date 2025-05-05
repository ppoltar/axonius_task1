# Makefile

.PHONY: build test install

# Build the Docker image
build:
	docker build -t my-test-container .

# Run tests inside the container
test:
	docker run --rm -v $(PWD)/reports:/app/reports my-test-container

# Install dependencies, build the container, and run tests
install: build test