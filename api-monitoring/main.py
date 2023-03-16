from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import numpy as np

app = Flask(__name__)
metrics = PrometheusMetrics(app)


# static information as metric
metrics.info("app_info", "Application info", version="1.0.3")


@app.route("/health")
def health():
    return {"health": "OK"}


@app.route("/predict", methods=["POST"])
def predict():
    result_ = np.random.randint(1, 100)
    return {"result": result_}
