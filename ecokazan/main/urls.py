from django.urls import path
from .views import *


urlpatterns = [

  path('', index, name='home'),
  path('map/', map, name='map'),
  path('map/favorites/', add_to_favorites, name='add_to_favorites'),
  path('calendar/', calendar, name='calendar'),
  path('social/signup/', signup_redirect, name='signup_redirect')
]

