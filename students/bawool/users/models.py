from django.db import models

# Create your models here.

class User(models.Model): 
    name     = models.CharField(max_length=40, unique=True)
    email    = models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=40)
    phone    = models.CharField(max_length=40, unique=True)

    def __str__(self): 
        return self.name

    class Meta: 
        db_table = 'users'