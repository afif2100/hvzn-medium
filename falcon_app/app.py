import falcon
from common.health import HealthCheck


app = falcon.App()
health = HealthCheck()

# endpoint
endpoint_prefix = "api/v1"

# app route
app.add_route('/health', health)
