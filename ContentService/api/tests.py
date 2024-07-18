from django.test import TestCase

# Create your tests here.
import random
from django.core.management.base import BaseCommand
from faker import Faker
from api.models import User, Car, AboutAttribute, SellerAttribute, Image


def handle():
    fake = Faker()

    # Generate dummy users
    for _ in range(10):
        user = User.objects.create_user(
            email=fake.email(),
            username=fake.user_name(),
            name=fake.first_name(),
            last_name=fake.last_name(),

        )

        # Generate dummy cars for each user
        for _ in range(5):
            car = Car.objects.create(
                scraped_text=fake.text(max_nb_chars=300),
                liked=random.choice([True, False]),
                seen=random.choice([True, False]),
                description=fake.text(max_nb_chars=3000),
                date=fake.date(),
                price=fake.random_number(digits=5),
                model=fake.word(),
                place=fake.city(),
                miles=fake.random_number(digits=6),
                link=fake.url(),
                year=fake.year(),
                score=random.uniform(0, 10),
                user=user
            )

            # Generate dummy about attributes for each car
            for _ in range(3):
                AboutAttribute.objects.create(
                    text=fake.text(max_nb_chars=1500),
                    car=car
                )

            # Generate dummy seller attributes for each car
            for _ in range(3):
                SellerAttribute.objects.create(
                    text=fake.text(max_nb_chars=1500),
                    car=car
                )

            # Generate dummy images for each car
            for _ in range(5):
                Image.objects.create(
                    link=fake.image_url(),
                    car=car
                )
