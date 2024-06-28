from django.urls import path
from .views import *

urlpatterns = [
  path('', store, name='stores'),
  path('<int:pk>', StoreDetailView.as_view(), name='store-detail'),
  path('like/', LikeStoreCreateView.as_view(), name='like'),
  path('rating/', RatingCreateView.as_view(), name='rating'),
]