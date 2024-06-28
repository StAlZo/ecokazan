from django.contrib import admin
from .models import Stores, LikeStore, RatingStore

admin.site.register(Stores)
admin.site.register(LikeStore)
admin.site.register(RatingStore)