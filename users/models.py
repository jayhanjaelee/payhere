from django.db import models


class User(models.Model):
    email = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=100)
    age = models.IntegerField(default=None, null=True, blank=True)
    phone_number = models.CharField(max_length=13, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
