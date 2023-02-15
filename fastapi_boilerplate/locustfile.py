from locust import HttpUser, between, task


class Prediction(HttpUser):
    wait_time = between(1, 1)

    @task
    def health(self):
        self.client.get("/health")

    @task
    def predict(self):
        headers = {"Content-Type": "application/json"}
        payload = {"age": 100, "bmi": 10}
        self.client.post("/predict", json=payload, headers=headers)
