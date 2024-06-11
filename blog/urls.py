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
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('comment/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
