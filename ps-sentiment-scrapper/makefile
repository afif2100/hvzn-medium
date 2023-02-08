APP_FILE=app
# IMAGE_NAME=gcr.io/hvzn-development/fastapi-app/app
IMAGE_NAME=afif2100/sentiment-playstore-banking
TAG=latest
PORT=8001

app:
	uvicorn $(APP_FILE):app --host 0.0.0.0 --port $(PORT) --reload --workers 4

batch:
	python get-data-ingestion-predict.py

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

push:
	docker push $(IMAGE_NAME):$(TAG)

run:
	docker run -it --rm -p $(PORT):$(PORT) $(IMAGE_NAME):$(TAG)

bash:
	docker run -it --rm $(IMAGE_NAME):$(TAG) bash

clean:
	docker rmi $(IMAGE_NAME):$(TAG)