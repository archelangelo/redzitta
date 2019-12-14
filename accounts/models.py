from django.db import models
from django.contrib import auth

class User(auth.models.User):

    class Meta:
        proxy = True

    def __str__(self):
        return "@{}".format(self.username)