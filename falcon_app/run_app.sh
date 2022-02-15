#!bin/bash/

export APP_PORT=6000

gunicorn app:app -b 0.0.0.0:$APP_PORT