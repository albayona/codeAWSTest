# import serializer from rest_framework
from rest_framework import serializers

# import model from models.py
from .models import Car, User


# Create a model serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'name')


# Create a model serializer
class CarSerializer(serializers.ModelSerializer):
    # specify model and fields
    images = serializers.StringRelatedField(many=True)
    about = serializers.StringRelatedField(many=True)
    seller = serializers.StringRelatedField(many=True)

    class Meta:
        model = Car
        fields = (
            'id', 'scraped_text', 'description', 'date', 'price', 'model', 'place', 'miles', 'link', 'year', 'score',
            'images', 'about', 'seller')
