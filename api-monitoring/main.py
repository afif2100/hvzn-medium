from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
import numpy as np
import asyncio
from loguru import logger

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# static information as metric
metrics.info("app_info", "Application info", version="1.0.3")


@app.route("/health")
async def health():
    return {"health": "OK"}


@app.route("/predict", methods=["POST"])
async def predict():
    rand_nums = np.random.uniform(low=0.001, high=0.3, size=(1,))[0]
    rand_nums = round(rand_nums, 4)
    logger.info(f"Sleep for {rand_nums}s")
    await asyncio.sleep(float(rand_nums))
    return {"result": str(rand_nums)}


if __name__ == "__main__":
    app.run(debug=True, port="5000")
