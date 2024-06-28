from django.contrib import messages
from django.shortcuts import render, redirect
from .models import RecyclingCenter, FavoritesRecyclingCenter
from django.views.generic import View
from django.core.serializers import serialize
from django.http import JsonResponse
from forum.models import SaveEvent


def index(request):
  return render(request, 'main/index.html', {'index_active': 'menu__item_active'})

def signup_redirect(request):
    messages.error(request, "Что-то пошло не так, возможно, вы уже имеете аккаунт")
    return redirect('sign_in')

def map(request):
  recycling_centers = RecyclingCenter.objects.all()
  favorites = FavoritesRecyclingCenter.objects.filter(user=request.user) if request.user.is_authenticated else None
  favorites_ids = [item.recycling_center.id for item in favorites] if favorites else 'None'
  data = {
      'recycling_centers': recycling_centers,
      'map_active': 'menu__item_active',
      'favorites': favorites_ids,
  }
  return render(request, 'main/map-page.html', data)


class FavoritesOnMapView(View):
    def get(self, request):
        favorites = FavoritesRecyclingCenter.objects.filter(user=request.user)
        data = [{'id': item.recycling_center.id} for item in favorites]
        return JsonResponse(data, safe=False)


def add_to_favorites(request):
    if request.method == 'POST' and request.user.is_authenticated:
        center_id = request.POST.get('center_id')
        center = RecyclingCenter.objects.get(id=center_id)
        user = request.user if request.user.is_authenticated else None
        if user and center:
            favorite, created = FavoritesRecyclingCenter.objects.get_or_create(
                recycling_center = center,
                user = user
            )
            if not created:
                favorite.delete()
                return JsonResponse({'status': 'deleted'})

            return JsonResponse({'status': 'created'})


def calendar(request):
    events_json = 'None'
    if request.user.is_authenticated:
        events = SaveEvent.objects.filter(user=request.user).select_related('event')
        events_list = [event.event for event in events]
        events_json = serialize('json', events_list)
    data = {
        'events': events_json,
        'calendar_active': 'menu__item_active'
    }
    return render(request, 'main/calendar-page.html', data)

