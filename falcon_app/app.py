import falcon
from common.health import HealthCheck
from api.hello_name import HelloName

app = falcon.App()
health = HealthCheck()
Name = HelloName()

# endpoint
endpoint_prefix = "api/v1"

# app route
app.add_route('/health', health)
app.add_route(f'/{endpoint_prefix}/hello', Name)
