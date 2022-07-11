from django.db import models
from django.db.models import Q

class UserQuerySet(models.QuerySet):
    def is_existed(self, data):
        return self.filter(Q(email=data)|Q(phone_number=data))

class UserManager(models.Manager):
    def get_queryset(self):
        return UserQuerySet(self.model, using=self._db)

    def is_existed(self, data):
        return self.get_queryset().is_existed(data)

class User(models.Model):
    name         = models.CharField(max_length=100)
    email        = models.CharField(max_length=100, unique=True)
    password     = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100, unique=True)
    create_at    = models.DateTimeField(auto_now_add=True)
    update_at    = models.DateTimeField(auto_now=True)

    objects      = UserManager()

    class Meta:
        db_table = 'users'