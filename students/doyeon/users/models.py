from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'