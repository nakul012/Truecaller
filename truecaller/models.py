from django.db import models

from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
from django.contrib import admin


# class User(AbstractBaseUser):
#     username = models.CharField(null=False, max_length=50)
#     email = models.EmailField(blank=True, null=True)
#     # phone = models.CharField(max_length=10, blank=True, null=True)
#     is_active= models.BooleanField(default=False)

# class User(models.Model):
#     username = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)
#     phone = models.CharField(max_length=10, unique=True)

#     USERNAME_FIELD = 'username'


# class Profile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     phone = models.CharField(max_length=10, unique=True)
#     is_spam = models.BooleanField(default=False)


# class Name(models.Model):
#     name = models.CharField(null=False, max_length=50)
#     profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

# def __str__(self):
#     return self.name


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=50, null=False)

    phone_number = models.IntegerField(null=False)
    email = models.EmailField(max_length=50, null=True)
    spam = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    phone_number = models.IntegerField(null=False, unique=True)
    email = models.EmailField(max_length=50, null=True)
    spam = models.BooleanField(default=False)


class UserPersonalContact(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return str(self.user)+","+str(self.contact)


admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(UserPersonalContact)
