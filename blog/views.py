from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView

from .forms import EmailPostForm, CommentForm
from .models import Post, Comment

import os
from dotenv import load_dotenv

load_dotenv()


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post,
                             is_published=Post.Status.PUBLISHED,
                             slug=post,
                             time_published__year=year,
                             time_published__month=month,
                             time_published__day=day)

    comments = post.comments.filter(is_active=True)
    form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})



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


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_published=Post.Status.PUBLISHED)
    comment = None
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)  # создаем экземпляр класса но не сохраняем в БД
        comment.post = post  # назначаем пост комментарию
        comment.save()
    return render(request, 'blog/post/comment.html',
                   {'post': post, 'form': form, 'comment': comment})
