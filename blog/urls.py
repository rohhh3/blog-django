from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("category/<category>/", views.post_category, name="post_category"),
    path('register', views.register, name='blog-register')
]
