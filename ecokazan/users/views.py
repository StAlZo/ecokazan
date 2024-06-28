from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.serializers import serialize
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserForgotPasswordForm, UserSetNewPasswordForm
from django.contrib import messages
from .models import Profile
from django.views.generic import DetailView, UpdateView, View, DeleteView, CreateView
from store.models import LikeStore, Stores
from forum.models import SaveEvent
from main.models import FavoritesRecyclingCenter
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpView(CreateView):

    form_class = UserRegisterForm
    success_url = reverse_lazy('home')
    template_name = 'users/sign-up-page.html'

    def form_valid(self, form):
        user = form.save()
        birth_date = self.request.POST.get('birth_date')
        user.profile.birth_date = birth_date

        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, error)
        return super().form_invalid(form)


class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/sign-in-page.html'
    success_message = 'Успешная авторизация'

    def get_success_url(self):
        return reverse_lazy('home')


class LogoutUserView(LogoutView):
    next_page = 'home'


class ProfileDetailView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'users/profile-page.html'
    queryset = model.objects.all().select_related('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя: {self.object.user.username}'
        context['favorites'] = (LikeStore.objects.filter(user__id=self.object.user.id))
        context['favorites_centers'] = (FavoritesRecyclingCenter.objects.filter(user=self.object.user))[:3-len(context['favorites'])]
        events_json = 'None'
        if self.request.user.is_authenticated:
            events = SaveEvent.objects.filter(user=self.request.user).select_related('event')
            events_list = [event.event for event in events]
            events_json = serialize('json', events_list)
        context['events'] = events_json
        return context


def edit_profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user is not None:
        profile = get_object_or_404(Profile, user=user)
        if request.method == 'POST':
            try:
                avatar = request.FILES.get('avatar', profile.avatar)
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                gender = request.POST.get('gender')
                birth_date = request.POST.get('birth_date')

                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()

                profile.avatar = avatar
                profile.gender = gender
                profile.birth_date = birth_date
                profile.save()

                return redirect('profile_detail', user.id)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            data = {
                'profile': profile,
            }
            return render(request, 'users/profile-edit-page.html', data)


@login_required(login_url='/')
def favorites(request):
    user = request.user
    favorite_stores = LikeStore.objects.filter(user=user).select_related('store')
    favorite_centers = FavoritesRecyclingCenter.objects.filter(user=user).select_related('recycling_center')
    data = {
        'favorite_stores': favorite_stores,
        'favorite_centers': favorite_centers,
    }
    return render(request, 'users/favorities-page.html', data)


class RemoveStoreFromFavoriteView(LoginRequiredMixin, View):
    login_url = '/'

    def post(self, request, pk, *args, **kwargs):
        user = self.request.user
        favorite = get_object_or_404(LikeStore, pk=pk, user=user)
        favorite.delete()
        return JsonResponse({'status': 'success'})


class RemoveCenterFromFavoriteView(LoginRequiredMixin, View):
    login_url = '/'

    def post(self, request, pk, *args, **kwargs):
        user = self.request.user
        favorite = get_object_or_404(FavoritesRecyclingCenter, pk=pk, user=user)
        favorite.delete()
        return JsonResponse({'status': 'success'})


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):

    form_class = UserForgotPasswordForm
    template_name = 'users/password_reset.html'
    success_url = reverse_lazy('home')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/email/password_subject_reset_mail.txt'
    email_template_name = 'users/email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):

    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('home')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context