from datetime import timezone
from django.db import models

# Create your models here.

class User(models.Model): 
    name       = models.CharField(max_length=40,  unique=True)
    email      = models.CharField(max_length=200, unique=True)
    password   = models.CharField(max_length=40)
    phone      = models.CharField(max_length=40,  unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return self.name

    class Meta: 
        db_table = 'users'
