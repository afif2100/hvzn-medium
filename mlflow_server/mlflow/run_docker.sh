#!/bin/sh
#export PROJECT_ID=$(gcloud config list project --format "value(core.project)")
#export PROJECT_ID=big-booking-329103


export REPO_NAME=afif2100
export IMAGE_NAME=mlflow-server-gcloud
export IMAGE_TAG=latest
export IMAGE_URI=${REPO_NAME}/${IMAGE_NAME}:${IMAGE_TAG}
# export IMAGE_URI=gcr.io/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:${IMAGE_TAG}



echo "doker $1 : ${IMAGE_URI}"

if [ "$1" == "build" ]; then
    docker build --rm -t ${IMAGE_URI} . 
elif [ "$1" == "run" ]; then
    docker run -it \
    -v /home/jupyter/github/hvzn-medium/mlflow_server/mlflow/gcloud-credentials:/workdir/gcloud-credentials/ \
    --rm ${IMAGE_URI} $2
elif [ "$1" == "push" ]; then
    docker push ${IMAGE_URI}
elif [ "$1" == "pull" ]; then
    docker pull ${IMAGE_URI}
elif [ "$1" == "bash" ]; then
    docker run --rm -it --entrypoint bash ${IMAGE_URI}
else
    echo "try again"
fi