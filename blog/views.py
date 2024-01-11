from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post


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