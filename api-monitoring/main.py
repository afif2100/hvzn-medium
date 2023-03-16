from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import numpy as np
from time import sleep
from loguru import logger

app = Flask(__name__)
metrics = PrometheusMetrics(app)


# static information as metric
metrics.info("app_info", "Application info", version="1.0.3")


@app.route("/health")
def health():
    return {"health": "OK"}


@app.route("/predict", methods=["POST"])
def predict():
    rand_nums = np.random.uniform(low=0.001, high=0.2, size=(1,))[0]
    rand_nums = round(rand_nums,4)
    logger.info(f"Sleep for {rand_nums}s")
    sleep(rand_nums)
    return {"result": str(rand_nums)}
