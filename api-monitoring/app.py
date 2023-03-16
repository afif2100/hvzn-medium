import time
from fastapi import FastAPI
from prometheus_client import Counter, Gauge, Histogram, start_http_server

# Define Prometheus metrics
REQUESTS = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "HTTP request latency", ["method", "endpoint"]
)
REQUEST_SIZE = Histogram(
    "http_request_size_bytes", "HTTP request size", ["method", "endpoint"]
)
RESPONSE_SIZE = Histogram(
    "http_response_size_bytes", "HTTP response size", ["method", "endpoint"]
)
ACTIVE_REQUESTS = Gauge("http_active_requests", "Number of active HTTP requests")

# Create FastAPI app
app = FastAPI()

# Define middleware to track Prometheus metrics
@app.middleware("http")
async def monitor_requests(request, call_next):
    # Record start time and active requests
    REQUEST_LATENCY.labels(request.method, request.url.path).observe(0)
    REQUEST_SIZE.labels(request.method, request.url.path).observe(
        len(await request.body())
    )
    ACTIVE_REQUESTS.inc()

    try:
        # Process request and record metrics
        response = await call_next(request)
        REQUESTS.labels(request.method, request.url.path, response.status_code).inc()
    finally:
        # Record end time and active requests
        REQUEST_LATENCY.labels(request.method, request.url.path).observe(time.time())
        ACTIVE_REQUESTS.dec()

    return response


# Define application routes
@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
@app
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


# Start Prometheus server
start_http_server(8000)
