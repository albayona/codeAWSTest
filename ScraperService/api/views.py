# Create your views here.
from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from .utils.jwt_user_authorization import get_user_from_header
from .utils.scraper import Scraper


@api_view(["POST"])
@get_user_from_header
def scrape_posts_view(request):
    try:
        token = request.headers.get('Authorization')
        if not token:
            return HttpResponseBadRequest('Token is missing from headers')

        r = JSONParser().parse(request)
        username = "ricardobayonalatorre@yahoo.com"
        password = "MiaGordo5"
        bot = Scraper(token, request.user, username, password)
        bot.scrape_posts(r['link'], 28)

        return JsonResponse({'status': 'success', 'scrape_url': r['link']})

    except Exception as e:
        return HttpResponseBadRequest(f'Error: {e}')
