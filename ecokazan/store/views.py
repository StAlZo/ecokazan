from django.shortcuts import render
from .models import Stores, LikeStore, RatingStore
from django.views.generic import DetailView, View
from django.http import JsonResponse



def store(request):
    stores = Stores.objects.all()
    if request.user.is_authenticated:
        ratings = RatingStore.objects.filter(user=request.user)
        likes = LikeStore.objects.filter(user=request.user)
        liked_store_ids = likes.values_list('store', flat=True)
    else:
        ratings = None
        liked_store_ids = None
    data = {
        'stores': stores,
        'ratings': ratings,
        'likes': liked_store_ids,
        'store_active': 'menu__item_active',
    }
    return render(request, 'store/shops-page.html', data)

class StoreDetailView(DetailView):
    model = Stores
    template_name = 'store/old/store_view.html'
    context_object_name = 'store'


class LikeStoreCreateView(View):
    model = LikeStore

    def post(self, request, *args, **kwargs):
        store_id = request.POST.get('store_id')
        user = request.user if request.user.is_authenticated else None
        if user:

            like, created = self.model.objects.get_or_create(
                store_id = store_id,
                user = user
            )

            if not created:
                like.delete()
                return JsonResponse({'status': 'deleted', 'likes_sum': like.store.get_sum_likes()})

            return JsonResponse({'status': 'created', 'likes_sum': like.store.get_sum_likes()})


class RatingCreateView(View):
    model = RatingStore

    def post(self, request, *args, **kwargs):
        store_id = request.POST.get('store_id')
        value = int(request.POST.get('value'))

        data_id = request.POST.get('data_id')

        user = request.user if request.user.is_authenticated else None

        if user:
            rating, created = self.model.objects.get_or_create(
                store_id=store_id,
                defaults={'value': value, 'user': user},
            )

            if not created:
                if rating.value == value:
                    rating.delete()
                    return JsonResponse({'status': 'deleted', 'rating_sum': rating.store.get_sum_rating()})
                else:
                    rating.value = value
                    rating.user = user
                    rating.save()
                    return JsonResponse({'status': 'updated', 'rating_sum': rating.store.get_sum_rating()})
            return JsonResponse({'status': 'created', 'rating_sum': rating.store.get_sum_rating()})
