from django.urls import path

from . import views
app_name = 'store'

urlpatterns = [
    path('', views.postcard_list, name='store'),
    path('category/<slug:category_slug>/', views.postcard_list,
         name='store_by_category'),
    path('<slug:slug>/', views.postcard_detail, name='postcard_detail'),
]