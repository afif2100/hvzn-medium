from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)


# static information as metric
metrics.info("app_info", "Application info", version="1.0.3")


@app.route("/")
def index():
    return {"hello": "world"}
