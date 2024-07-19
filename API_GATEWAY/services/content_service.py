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


    '''
    curl -i -s -X POST localhost:8001/services --data 'name=auth_service' --data 'url=http://3.20.227.39:8080'
   
    curl -i -s -X POST localhost:8001/services/auth_service/routes --data 'paths[]=/token/' --data name=token
    
    
    curl -X POST http://localhost:8001/services/pub_service/plugins \
   --header "accept: application/json" \
   --header "Content-Type: application/json" \
   --data '
   {
 "name": "cors",
 "config": {
   "origins": [
     "*"
   ],
   "methods": [
     "GET",
     "POST"
   ],
   "headers": [
     "*"
   ],
   "exposed_headers": [
     "*"
   ],
   "credentials": true,
   "max_age": 3600
 }
}




curl -i -X PATCH http://localhost:8001/plugins/05c24121-80f4-489d-862f-dbaeaf773b90 \
  --data "enabled=false"



curl -i -X POST http://localhost:8001/services/nlp_service/plugins \
  --data "name=jwt"
  
curl -i -X POST http://localhost:8001/services/content_service/plugins \
  --data "name=jwt"
  
curl -i -X POST http://localhost:8001/services/pub_service/plugins \
  --data "name=jwt"
  
curl -i -X POST http://localhost:8001/services/scrape_service/plugins \
  --data "name=jwt"
  


content_service
pub_service
scrape_service



   '

    
    
    
    
    '''

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
