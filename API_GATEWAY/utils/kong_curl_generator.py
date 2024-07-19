#!/usr/bin/env python3

def register_service(service_name, service_url, kong_base_url):
    command = (
        f"curl -i -s -X POST {kong_base_url}/services "
        f"--data 'name={service_name}' "
        f"--data 'url={service_url}'"
    )
    return command


def register_routes(service_name, kong_base_url, routes):
    commands = []
    for route in routes:
        path = f"/{route.replace('<int:iid>', '1').replace('<str:iid>', 'example_id')}"
        command = (
            f"curl -i -s -X POST {kong_base_url}/services/{service_name}/routes "
            f"--data 'paths[]={path}' "
            f"--data name={route.replace('/', '_').replace('-', '_')} "
        )
        commands.append(command)
    return commands


def handle_service_and_routes(kong_host, service_name, service_url, routes):
    kong_base_url = f"http://{kong_host}:8001"

    # Register the service
    service_command = register_service(service_name, service_url, kong_base_url)
    print("Register Service Command:")
    print(service_command)
    print()

    # Register routes
    route_commands = register_routes(service_name, kong_base_url, routes)
    print("Register Routes Commands:")
    for command in route_commands:
        print(command)


