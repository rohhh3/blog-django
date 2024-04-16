from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Comment(models.Model):
    datePosted = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    author = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.author
    
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
            return self.name
    
class Post(models.Model):
    isPublic = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    datePosted = models.DateTimeField(default=timezone.now)
    thumbnail = models.ImageField(upload_to='files/thumbnails', null=True)

    author = models.ForeignKey(User, on_delete=models.PROTECT) 
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True) 
    categories = models.ManyToManyField(Category) 

    def __str__(self):
        return self.title
        