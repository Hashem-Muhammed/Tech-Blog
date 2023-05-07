from django.db import models
from django.utils.text import slugify
from datetime import datetime
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Author(AbstractUser):
    email = models.EmailField(unique=True)
    profileImage = models.ImageField(null= True ,blank= True, default='default.jpg')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'password',
        
    ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    def save(self, *args, **kwargs):
        self.username= self.email
        super(Author,self).save(*args,**kwargs)    

class Tag(models.Model):
    content = models.CharField( max_length=30)
    


class Post(models.Model):
    
    title = models.CharField(max_length=100)
    date = models.DateTimeField(default=now)
    slug = models.SlugField()
    content = models.CharField( max_length=350)
    author = models.ForeignKey(Author, on_delete=models.CASCADE , related_name= "author")   
    tag = models.ManyToManyField(Tag) 
    postImage = models.ImageField(null= True ,blank= True)

    
    def __str__(self):
        return f"{self.title}"
    def save(self, *args, **kwargs):
        self.slug= slugify(self.title)
        super(Post,self).save(*args,**kwargs)
 

class Comment(models.Model):

    content = models.CharField(max_length=500)
    author = models.ForeignKey(Author, on_delete= models.CASCADE , related_name='comment_auhtor')
    post = models.ForeignKey(Post, on_delete= models.CASCADE , related_name='comment_post')


    def __str__(self):
        return f"{self.content}"



