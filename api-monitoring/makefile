APP_FILE=app
# IMAGE_NAME=gcr.io/hvzn-development/fastapi-app/app
IMAGE_NAME=afif2100/api-monitoring
TAG=latest
PORT=8000
MWD = /Users/hafizhan.aliady/Documents/GitHub/hvzn-medium
PROM_CONFIG=/Users/hafizhan.aliady/Documents/GitHub/hvzn-medium/api-monitoring/config
GRAFANA_CONFIG=/Users/hafizhan.aliady/Documents/GitHub/hvzn-medium/api-monitoring/config/grafana

app:
	gunicorn main:app --reload -b 0.0.0.0:8000

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

prom:
	docker run --rm -it \
	-p 9090:9090 \
	-v ${PROM_CONFIG}:/etc/prometheus \
	prom/prometheus

gf:
	docker run --rm -it \
	-p 3000:3000 \
	-v ${GRAFANA_CONFIG}:/var/lib/grafana \
	grafana/grafana-oss:latest