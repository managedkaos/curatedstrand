# Makefile

# Variables
IMAGE_NAME := curatedstrand

# Targets
test:
	pytest

install:
	pip install --requirement requirements.txt

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -p 8000:8000 $(IMAGE_NAME)

uvicorn:
	uvicorn main:app --host 0.0.0.0 --port 8000

clean:
	docker container prune --force
	docker image prune --force

.PHONY: install test build run uvicorn clean
