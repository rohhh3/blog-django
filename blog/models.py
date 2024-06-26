from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.core.files.storage import default_storage

# Create your models here.
class CustomUser(AbstractUser):
    STATUS = (
         ('regular', 'regular'),
         ('admin', 'admin')
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='regular')
    description = models.TextField('Description', max_length=600, default='', blank=True)
    avatar = models.ImageField(upload_to='images/avatars/', blank=True, null=True)

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        try:
            old_avatar = CustomUser.objects.get(id=self.id).avatar
        except CustomUser.DoesNotExist:
            old_avatar = None

        super().save(*args, **kwargs)

        if old_avatar and old_avatar != self.avatar:
            default_storage.delete(old_avatar.path)

class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
            return self.name
    
class Post(models.Model):
    isPublic = models.BooleanField(default=True)
    title = models.CharField(max_length=200, unique=True)
    content = RichTextField(blank=True, null=True, max_length=8000)
    datePosted = models.DateTimeField(default=timezone.now)
    thumbnail = models.ImageField(upload_to='images/thumbnails/', null=True, blank=True)

    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT) 
    categories = models.ManyToManyField("Category", related_name="posts") 
    password = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        if self.thumbnail:
            default_storage.delete(self.thumbnail.path)
        super().delete(*args, **kwargs)
    
class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    content = models.TextField()
    datePosted = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} on '{self.post}'"
        