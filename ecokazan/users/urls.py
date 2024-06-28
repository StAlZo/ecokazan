from django.urls import path
from .views import *
from django.contrib.auth import views as authViews
from django.conf import settings

urlpatterns = [
    path('sign_in/', LoginUserView.as_view(), name='sign_in'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('sign_out', LogoutUserView.as_view(), name='sign_out'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('favorites/', favorites, name='favorites'),
    path('remove_favorite_store/<int:pk>/', RemoveStoreFromFavoriteView.as_view(), name='remove_favorite'),
    path('remove_favorite_center/<int:pk>/', RemoveCenterFromFavoriteView.as_view(), name='remove_favorite_center'),
    path('edit/<int:pk>', edit_profile, name='profile-edit'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('exit/', authViews.LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='exit'),


]

