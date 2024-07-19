import KONG_SETTINGS
from utils.kong_curl_generator import register_service, register_routes


def main():
    kong_base_url = KONG_SETTINGS.HOST

    service_name = "content_service"
    service_url = "http://18.220.226.53:8000"
    routes = [
        "users/",
        "create/",
        "create-user/",
        "list-new/",
        "list-old/",
        "list-liked/",
        "list-discarded/",
        "like/",
        "unlike/",
        "see/",
        "see-all/",
        "empty-fav/",
        "unsee/"
    ]

    # Register the service
    service_command = register_service(service_name, service_url, kong_base_url)
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
