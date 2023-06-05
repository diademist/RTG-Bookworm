# Create your models here.
from django.conf import settings
from django.db import models

class StoredPassword(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False
    )
    password = models.CharField(
        'Password hash',
        max_length=255,
        editable=False
    )
    date = models.DateTimeField(
        'Date',
        auto_now_add=True,
        editable=False
    )

class BookForm(models.Model):
    bookname= models.CharField(max_length=100)
    author= models.CharField(max_length=50)
    genre= models.CharField(max_length=30)
    description= models.CharField(max_length=200)
    
