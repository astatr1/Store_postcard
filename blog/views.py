from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .forms import EmailPostForm
from .models import Post

import os
from dotenv import load_dotenv
load_dotenv()


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


class PostDetailView(DetailView):
    template_name = 'blog/post/detail.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return get_object_or_404(Post, slug=self.kwargs[self.slug_url_kwarg])


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_published=Post.Status.PUBLISHED)

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} рекомендует Вам к прочтению {post.title}"
            message = f"Ознакомиться с {post.title} по ссылке {post_url}\n\n" \
                f"{cd['name']} рекомендовал: {cd['comments']}"
            send_mail(subject, message, os.getenv('EMAIL_HOST'), [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',
                  {'post': post, 'form': form, 'sent': sent})
