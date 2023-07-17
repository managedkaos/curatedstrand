# Makefile

## Variables
IMAGE_NAME   := curatedstrand
VIRTUAL_ENV  := $(PWD)/venv

## Common
test:
	pytest

install:
	python -m pip install --upgrade pip
	pip install --requirement requirements.txt

index:
	mkdir -p ./_site
	sleep 2
	curl localhost:8000 > ./_site/index.html
	sleep 2

## Docker
build:
	docker build --tag $(IMAGE_NAME) .

run:
	docker run --publish 8000:8000 $(IMAGE_NAME)

detach:
	docker run --rm --detach --publish 8000:8000 --name $(IMAGE_NAME) $(IMAGE_NAME)

stop:
	docker stop $(IMAGE_NAME)

clean:
	docker container prune --force
	docker image prune --force

# Local
local: venv install uvicorn

venv: ./requirements.txt
	python -m venv $(VIRTUAL_ENV) || true

uvicorn:
	$(VIRTUAL_ENV)/bin/uvicorn main:app --host 0.0.0.0 --port 8000 || true

.PHONY: install test build run uvicorn clean
