# Login User
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import User
from api.serializers import MyTokenObtainPairSerializer, RegisterSerializer, UserSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Register User
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['GET'])
def list_user_view(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    print(request.headers)
    response = Response(serializer.data)

    return response
