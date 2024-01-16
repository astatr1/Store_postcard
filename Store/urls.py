from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

from postcard.views import page_not_found

sitemaps = {'post': PostSitemap}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('postcard.urls')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]


handler404 = page_not_found
