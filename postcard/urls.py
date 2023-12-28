from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostcardHome.as_view(), name='home'),
    path('postcard/<slug:postcard_slug>/', views.ShowPostcard.as_view(), name='postcard'),
]