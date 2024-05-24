from django.contrib import admin
from .models import Post, Comment, Category, CustomUser

# Register your models here.
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(CustomUser)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'datePosted' , 'isPublic') #dodatkowe kolumny do post
    list_filter = ('datePosted', 'isPublic')
    ordering = ('title',)
    search_fields = ('title', 'author', 'datePosted' , 'isPublic', 'categories')
    fields = (('title', 'author', 'isPublic'), 'content', 'categories', 'thumbnail', 'datePosted') #struktura formularza tworzenia/edytowania 

