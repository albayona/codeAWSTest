

APIGATE_WAY_KONG

#CONTENT_SERVICE

 curl -i -X POST http://localhost:8001/services/ \
  --data "name=dummy-service" \
  --data "url=http://google.com"
