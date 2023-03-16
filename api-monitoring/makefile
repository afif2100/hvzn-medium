APP_FILE=app
# IMAGE_NAME=gcr.io/hvzn-development/fastapi-app/app
IMAGE_NAME=afif2100/fastapi-app
TAG=latest
PORT=8000
MWD = /Users/hafizhan.aliady/Documents/GitHub/hvzn-medium
PROM_CONFIG=/Users/hafizhan.aliady/Documents/GitHub/hvzn-medium/api-monitoring/config

app:
	#uvicorn app:app --reload
	gunicorn main:app --reload -b 0.0.0.0:8000

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

push:
	docker push $(IMAGE_NAME):$(TAG)

run:
	docker run -it -d --name ubuntu --platform=linux/amd64 -v $(MWD):/home --rm ubuntu-merlin-migration:latest

bash:
	docker run -it --rm $(IMAGE_NAME):$(TAG) bash

clean:
	docker rmi $(IMAGE_NAME):$(TAG)

monitor:
	docker run --rm -it \
	-p 9090:9090 \
	-v ${PROM_CONFIG}:/etc/prometheus \
	prom/prometheus
