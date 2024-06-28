from django.urls import path
from .views import *

urlpatterns = [
  path('', forum, name='forum'),
  path('<int:pk>/', NewsDetailView.as_view(), name='forum-detail'),
  path('<int:pk>/comments/create/', add_comment, name='comment_create'),
  path('save/', SaveEventCreateView.as_view(), name='save'),
]

