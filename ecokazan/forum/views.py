from django.shortcuts import render
from .models import Articles, Comment, SaveEvent
from django.views.generic import DetailView, View
from .forms import CommentForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse



def forum(request):
    news = Articles.objects.order_by('-data')[:3]
    comment_dict = []
    for new in news:
        comment_dict.append({ new: Comment.objects.filter(article=new) })
    data ={
        'news': news,
        'comments': comment_dict,
        'forum_active': 'menu__item_active',
    }
    return render(request, 'forum/forum-page.html', data)


class NewsDetailView(DetailView):
    model = Articles
    template_name = 'forum/single-post-page.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['comments'] = Comment.objects.filter(article=self.object)
        context['comment_form'] = CommentForm
        context['forum_active'] = 'menu__item_active'
        if SaveEvent.objects.filter(event=self.object).count() > 0:
            saves = True
        else:
            saves = False
        context['saves'] = saves
        return context


@login_required
@require_http_methods(["POST"])
def add_comment(request, pk):
    form = CommentForm(request.POST)
    article = get_object_or_404(Articles, id=pk)

    if form.is_valid():
        comment = Comment()
        comment.article = article
        comment.author = auth.get_user(request)
        comment.content = form.cleaned_data['content']
        comment.save()

    return redirect(article.get_absolute_url())


class SaveEventCreateView(View):
    model = SaveEvent

    def post(self, request, *args, **kwargs):
        event_id = request.POST.get('event_id')
        user = request.user if request.user.is_authenticated else None
        if user:
            save, created = self.model.objects.get_or_create(
                event_id = event_id,
                user = user
            )

            if not created:
                # like_count = like.store.get_sum_likes - 1
                save.delete()
                return JsonResponse({'status': 'deleted', 'save_sum': save.event.get_sum_saves()})

            return JsonResponse({'status': 'created', 'save_sum': save.event.get_sum_saves()})