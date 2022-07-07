from django.db import models

class User(models.Model):
    name         = models.CharField(max_length=50)
    email        = models.CharField(max_length=50, unique=True)
    password     = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=50)

    class Meta:
        db_table = 'users'