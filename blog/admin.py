from django.contrib import admin
from .models import Post, Comment, Category, CustomUser

# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'post', 'datePosted')
    list_filter = ('datePosted', )
    ordering = ('datePosted', )
    search_fields = ('author', 'content', 'post')
    fields = (('author', 'post'), 'content','datePosted')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email','first_name', 'last_name', 
                    'date_joined', 'last_login')
    list_filter = ('is_active', 'is_staff', 'last_login', 'date_joined')
    ordering = ('date_joined',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fields = (('email','username', 'password'), ('first_name', 'last_name'),
              'status',('is_staff','is_superuser', 'is_active'), 'avatar','description', 
              ('groups', 'user_permissions'))

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'datePosted' , 'isPublic') #dodatkowe kolumny do post
    list_filter = ('datePosted', 'isPublic') #filtrowanie
    ordering = ('title',)
    search_fields = ('title', 'author__username')
    fields = (('title', 'author', 'isPublic'), 'content', 'categories', 'thumbnail', 'datePosted') #struktura formularza tworzenia/edytowania 

