from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class CustomUser(AbstractUser):
    STATUS = (
         ('regular', 'regular'),
         ('admin', 'admin')
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='regular')
    description = models.TextField('Description', max_length=600, default='', blank=True)
    avatar = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username

class Comment(models.Model):
    datePosted = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT)

    def __str__(self):
        return self.author
    
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
            return self.name
    
class Post(models.Model):
    isPublic = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=1000)
    datePosted = models.DateTimeField(default=timezone.now)
    thumbnail = models.ImageField(upload_to='files/thumbnails', null=True)

    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT) 
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True) 
    categories = models.ManyToManyField(Category) 

    def __str__(self):
        return self.title
        