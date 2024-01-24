from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from taggit.models import Tag
from django.db.models import Count

from .forms import EmailPostForm, CommentForm
from .models import Post, Comment

import os
from dotenv import load_dotenv

load_dotenv()


# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'

def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
 # Постраничная разбивка с 3 постами на страницу
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
# Если page_number не целое число, то выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:
 # Если page_number находится вне диапазона, то выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html',
                  {'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post,
                             is_published=Post.Status.PUBLISHED,
                             slug=post,
                             time_published__year=year,
                             time_published__month=month,
                             time_published__day=day)

    comments = post.comments.filter(is_active=True)
    form = CommentForm()
    # Получение схожих постов по тегам
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                        .order_by('-same_tags', '-time_published')[:4]
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})


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
