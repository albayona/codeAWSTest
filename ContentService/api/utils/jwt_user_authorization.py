##
import json
from functools import wraps

import jwt
from django.http import JsonResponse
from jwt import ExpiredSignatureError, InvalidTokenError
from cryptography.hazmat.primitives import serialization

from api.models import User


def remove_bearer_prefix(token_str):
    if token_str.startswith("Bearer "):
        return token_str[len("Bearer "):]
    else:
        return token_str


def get_user_from_jwt(token):
    token = remove_bearer_prefix(token)

    with open("jwtRS256.key.pub", "rb") as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())

        try:
            # Decode the JWT
            decoded_jwt = jwt.decode(token, public_key, algorithms=["RS256"])
            decoded_jwt_json = json.loads(decoded_jwt)
            return decoded_jwt_json['email']

        except ExpiredSignatureError:
            raise ExpiredSignatureError("Token has expired")

        except InvalidTokenError:
            raise InvalidTokenError("Invalid token")


def get_user_from_header(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_email = request.headers.get('X-Consumer-Custom-Id')
        print(user_email)
        if not user_email:
            return JsonResponse({'error': 'X-Consumer-Custom-Id header is missing'}, status=400)
        try:
            user = User.objects.get(email=user_email)
            request.user = user  # Attach the user object to the request
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found in content service'}, status=404)

        return view_func(request, *args, **kwargs)

    return _wrapped_view
