from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=20),
    email        = models.EmailField(max_length=250, unique=True),
    password     = models.CharField(max_length=300),
    phone_number = models.IntegerField(max_length=50)

    class Meta:
        db_table = 'users'
