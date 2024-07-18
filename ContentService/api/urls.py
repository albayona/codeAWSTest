from django.urls import path

# import everything from views
from .views import *

urlpatterns =[
    path('', content_service, name='content_service'),
    path('populate/', create_dummy_data, name='populate'),
    path('users/', get_users, name='users'),
    path('create/', create_car_view, name='create'),
    path('create-user/', create_user, name='create_user'),
    path('list-new/', list_new_view, name='list_new'),
    path('list-old/', list_old_view, name='list_old'),
    path('list-liked/', list_liked_view, name='list_liked'),
    path('list-discarded/', list_discarded_view, name='list_discarded'),
    path('like/<int:iid>', like_view, name='like'),
    path('unlike/<int:iid>', unlike_view, name='unlike'),
    path('see/<str:iid>', mark_seen_view, name='see'),
    path('see-all/', see_all_view, name='see_all'),
    path('empty-fav/', empty_fav_view, name='empty_fav'),
    path('unsee/<int:iid>', unmark_seen_view, name='unsee'),
    path('discard/<int:iid>', discard_view, name='discard'),
    path('undiscard/<int:iid>', undiscard_view, name='undiscard'),
]