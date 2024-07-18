from django.urls import path

# import everything from views
from .views import *

urlpatterns =[
    path('scrape/', scrape_posts_view, name='scrape'),

]