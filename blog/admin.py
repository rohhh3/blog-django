from django.contrib import admin
from .models import Post, Comment, Category, CustomUser

# Register your models here.
admin.site.register(Comment)
admin.site.register(CustomUser)

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

