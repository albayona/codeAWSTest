import json

import requests
from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response

from SSEBroker import BASE_URL
from api.models import Car, User, AboutAttribute, SellerAttribute, Image
from api.serializers import CarSerializer, UserSerializer
from api.tests import handle
from api.utils.jwt_user_authorization import get_user_from_header




@api_view(["POST"])
def create_dummy_data(request):
    handle()
    return JsonResponse({'data create': True}, status=200)


@api_view(["POST"])
def create_user(request):
    try:
        # Parse JSON data from the request body
        data = json.loads(request.body)
        # Extract fields
        email = data.get('email')
        name = data.get('name')
        last_name = data.get('last_name')

        # Validate required fields
        if not email or not name:
            return JsonResponse({'error': 'Email and name are required'}, status=400)

        # Create a new user
        user = User.objects.create(email=email, name=name, last_name=last_name)

        # Return success response with user data
        return JsonResponse({
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'last_name': user.last_name
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@api_view(["POST"])
@get_user_from_header
def create_car_view(request):
    try:
        # Parse JSON data from the request body
        data = json.loads(request.body)
        about_data = data.get('about', [])
        seller_desc_data = data.get('seller_desc', [])
        images_data = data.get('images', [])

        # Create Car object
        car = Car.objects.create(
            scraped_text=data.get('scraped_text', ''),
            description=data.get('description', ''),
            date=data.get('date', ''),
            price=data.get('price', 0),
            model=data.get('model', ''),
            place=data.get('place', ''),
            miles=data.get('miles', 0.0),
            link=data.get('link', ''),
            year=data.get('year', 0),
            score=data.get('score', 0.0),
            user=request.user
        )

        # Create AboutAttribute objects
        for about_text in about_data:
            AboutAttribute.objects.create(
                text=about_text,
                car=car
            )

        # Create SellerAttribute objects
        for seller_text in seller_desc_data:
            SellerAttribute.objects.create(
                text=seller_text,
                car=car
            )

        # Create Image objects
        for image_url in images_data:
            Image.objects.create(
                link=image_url,
                car=car
            )

        user_email = request.user.email  # Example user ID
        pub_event_url = f'{BASE_URL}/{car.id}'
        headers = {"user": {user_email}}

        response = requests.post(pub_event_url, headers=headers)

        return JsonResponse({'status': 'success', 'car_id': car.id, 'event_url': pub_event_url, 'response': response.text})

    except KeyError as e:
        return HttpResponseBadRequest(f'Missing key: {e}')
    except Exception as e:
        return HttpResponseBadRequest(f'Error: {e}')

@api_view(["GET"])
@get_user_from_header
def get_user(request):
    user = request.user
    serializer = UserSerializer(user)
    response = Response(serializer.data)

    return response

@api_view(["GET"])
def content_service(request):
    return JsonResponse({'ContentService running': True}, status=200)

@api_view(["GET"])
def get_users(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    response = Response(serializer.data)
    return response


@api_view(["GET"])
@get_user_from_header
def list_new_view(request):
    user = request.user
    cars = Car.objects.filter(seen=False, user=user).order_by('score')

    serializer = CarSerializer(cars, many=True)
    response = Response(serializer.data)
    return response


@api_view(["GET"])
@get_user_from_header
def list_old_view(request):
    user = request.user
    cars = Car.objects.filter(seen=True, user=user).order_by('score')

    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@get_user_from_header
def list_liked_view(request):
    user = request.user
    cars = Car.objects.filter(liked=True, user=user).order_by('score')
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@get_user_from_header
def list_discarded_view(request):
    user = request.user
    cars = Car.objects.filter(discarded=True, user=user).order_by('score')
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


@api_view(["PUT"])
@get_user_from_header
def see_all_view(request):
    user = request.user
    Car.objects.filter(seen=False, user=user).update(seen=True)
    return JsonResponse({'status': 'success', 'all archived': True})


@api_view(["PUT"])
@get_user_from_header
def empty_fav_view(request):
    user = request.user
    Car.objects.filter(liked=True, user=user).update(liked=False)
    return JsonResponse({'status': 'success', 'favorites emptied': True})


@api_view(["PUT"])
@get_user_from_header
def like_view(request, iid):
    user = request.user
    if iid:
        try:
            car = Car.objects.get(pk=iid, user=user)
            car.liked = True
            car.seen = True
            car.save()
            return JsonResponse({'status': 'success', 'iid': iid, 'liked': True})
        except Car.DoesNotExist:
            return JsonResponse({'error': 'Car not found'}, status=404)
    return JsonResponse({'error': 'IID is required'}, status=400)


@api_view(["PUT"])
@get_user_from_header
def unlike_view(request, iid):
    user = request.user
    if iid:
        try:
            car = Car.objects.get(pk=iid, user=user)
            car.liked = False
            car.seen = True
            car.save()
            return JsonResponse({'status': 'success', 'iid': iid, 'liked': False})
        except Car.DoesNotExist:
            return JsonResponse({'error': 'Car not found'}, status=404)
    return JsonResponse({'error': 'IID is required'}, status=400)


@api_view(["PUT"])
@get_user_from_header
def mark_seen_view(request, iid):
    user = request.user
    if iid:
        try:
            car = Car.objects.get(pk=iid, user=user)
            car.seen = True
            car.save()
            return JsonResponse({'status': 'success', 'iid': iid, 'seen': True})
        except Car.DoesNotExist:
            return JsonResponse({'error': 'Car not found'}, status=404)
    return JsonResponse({'error': 'IID is required'}, status=400)


@api_view(["PUT"])
@get_user_from_header
def unmark_seen_view(request, iid):
    user = request.user
    if iid:
        try:
            car = Car.objects.get(pk=iid, user=user)
            car.seen = False
            car.save()
            return JsonResponse({'status': 'success', 'iid': iid, 'seen': False})
        except Car.DoesNotExist:
            return JsonResponse({'error': 'Car not found'}, status=404)
    return JsonResponse({'error': 'IID is required'}, status=400)


@api_view(["PUT"])
def discard_view(request, iid):
    if iid:
        try:
            car = Car.objects.get(pk=iid)
            car.discarded = True
            car.save()
            return JsonResponse({'status': 'success', 'iid': iid, 'discarded': True})
        except Car.DoesNotExist:
            return JsonResponse({'error': 'Car not found'}, status=404)
    return JsonResponse({'error': 'IID is required'}, status=400)


@api_view(["PUT"])
def undiscard_view(request, iid):
    if iid:
        try:
            car = Car.objects.get(pk=iid)
            car.discarded = False
            car.save()
            return JsonResponse({'status': 'success', 'iid': iid, 'discarded': False})
        except Car.DoesNotExist:
            return JsonResponse({'error': 'Car not found'}, status=404)
    return JsonResponse({'error': 'IID is required'}, status=400)
