from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.home, name='blog-home'),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("category/<category>/", views.post_category, name="post_category"),
    path('register', views.register, name='blog-register'),
    path('login', views.user_login, name='blog-login'),
    path('logout', views.user_logout, name='logout'),
    path('post/new/', views.post_new, name='post_new'),
    path('update_user', views.update_user, name='update_user'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
