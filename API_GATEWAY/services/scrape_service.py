import KONG_SETTINGS
from utils.kong_curl_generator import register_service, register_routes


def main():
    kong_base_url = kong_base_url = KONG_SETTINGS.HOST

    upstream_name = "nlp_service_upstream"
    service_url1 = "3.135.1.255:8000"
    service_url2 = "18.219.59.53:8000"
    service_name = "nlp_service"

    routes = [
        "scrape-nlp/"
    ]

    upstream_command = f'''
curl -X POST localhost:8001/upstreams \
 --data name={upstream_name}

curl -X POST localhost:8001/upstreams/{upstream_name}/targets \
  --data target='{service_url1}'
  
curl -X POST localhost:8001/upstreams/{upstream_name}/targets \
  --data target='{service_url2}'
  
  curl -X PATCH http://localhost:8001/services/{service_name} \
  --data host='{upstream_name}'

    '''

    print(f"Register Upstream Command for {upstream_name}:")
    print(upstream_command)

    # Register the service
    service_command = register_service(service_name, "http://httpbin.org", kong_base_url)
    print(f"Register Service Command for {service_name}:")
    print(service_command)
    print()

    # Register routes
    route_commands = register_routes(service_name, kong_base_url, routes)
    print(f"Register Routes Commands for {service_name}:")
    for command in route_commands:
        print(command)


if __name__ == "__main__":
    main()
