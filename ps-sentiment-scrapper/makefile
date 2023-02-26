APP_FILE=app
# IMAGE_NAME=gcr.io/hvzn-development/fastapi-app/app
IMAGE_NAME=afif2100/sentiment-playstore-banking
TAG=latest
HOST=0.0.0.0
PORT=8001

app:
	uvicorn $(APP_FILE):app --host ${HOST} --port $(PORT) --reload --workers 4

home:
	streamlit run home.py
	pyclean .

batch:
	python process_batch.py
	pyclean .

sync-bq:
	python experiment/sync_with_bq.py

download-model:
	git clone https://huggingface.co/sahri/indonesiasentiment models

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

push:
	docker push $(IMAGE_NAME):$(TAG)

run:
	docker run -it --rm -e PG_HOST=db-1 -p $(PORT):$(PORT) --hostname host $(IMAGE_NAME):$(TAG) 

bash:
	docker run -it --rm $(IMAGE_NAME):$(TAG) bash

clean:
	docker rmi $(IMAGE_NAME):$(TAG)