
API_GATEWAY_HOST = "http://localhost:8000"

# CONTENT_SERVICE

CONTENT_SERVICE_HOST = "http://localhost:8001"
CONTENT_SERVICE_name = "content_service"
f'''
 curl -i -X POST {API_GATEWAY_HOST}/services/ \
  --data "name={CONTENT_SERVICE_name}" \
  --data "url={CONTENT_SERVICE_HOST}"
'''
