APP_FILE=app
# IMAGE_NAME=gcr.io/hvzn-development/fastapi-app/app
IMAGE_NAME=afif2100/fastapi-app
TAG=latest
PORT=8000


run:
	uvicorn $(APP_FILE):app --host 0.0.0.0 --port $(PORT) --reload --workers 10
# gunicorn $(APP_FILE):app -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker
