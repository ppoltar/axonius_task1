install:
	python3 -m venv venv && \
	source venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt

test:
	venv/bin/pytest --suite-timeout=900