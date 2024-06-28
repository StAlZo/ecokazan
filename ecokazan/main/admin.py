from django.contrib import admin
from .models import RecyclingCenter, FavoritesRecyclingCenter

# Register your models here.

admin.site.register(RecyclingCenter)
admin.site.register(FavoritesRecyclingCenter)
