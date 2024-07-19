import json

import requests
from django.contrib.auth.password_validation import validate_password
from django.core.serializers.json import DjangoJSONEncoder

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from AuthService.settings import API_GATEWAY
from api.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('iss', 'username', 'email', 'role', 'iss')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['iss'] = str(user.iss)

        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = None
        try:

            user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email'],
                role='admin'
            )

            user.set_password(validated_data['password'])
            user.save()

            self.create_consumer(validated_data)
            self.create_jwt_credentials(validated_data, user.iss)

            return user

        except Exception as e:
            if user:
                user.delete()
            # Handle HTTP errors or connection issues
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create_jwt_credentials(self, validated_data, iss):
        with open('jwtRS256.key.pub', 'rb') as public_key_file:

            files = {
                'rsa_public_key': ('jwtRS256.key.pub', public_key_file)
            }

            data = {
                'key': iss,
                'algorithm': 'RS256',
            }

            jwt_response = requests.post(f"{API_GATEWAY}/consumers/{validated_data['email']}/jwt", files=files,
                                         data=data)

            if jwt_response.status_code == 201:
                res = jwt_response.json()
                print('RSA public key added successfully.')
                print('Response:', res)

            else:
                raise Exception(
                    f'Failed to add RSA public key. Status code: {jwt_response.status_code}, Response: {jwt_response.text}'
                )

    def create_consumer(self, validated_data):
        # The data to be sent in the POST request
        data = {
            'username': validated_data['email'],
            'custom_id': validated_data['email'],
        }
        # Send the POST request to Kong Admin API
        consumer_response = requests.post(f"{API_GATEWAY}/consumers/", data=data)
        # Check the consumer_response status and content
        if consumer_response.status_code == 201:
            print('Consumer created successfully.')
            print('Response:', consumer_response.json())
        else:
            raise Exception(
                f'Failed to create consumer.: {consumer_response.status_code}, Response: {consumer_response.text}'
            )
