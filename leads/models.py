from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


# 'Model' is a class in models file in django-framework so when we inherit from it,
# now then our Lead class is a Model too.
class Lead(models.Model):  # Lead is one of our database tables.
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    organization = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    agent = models.ForeignKey('Agent', null=True, blank=True,
                              on_delete=models.SET_NULL)  # 'Agent' because our Agent model is under this Lead model
    category = models.ForeignKey('Category', null=True, blank=True,
                                 related_name='leads',
                                 on_delete=models.SET_NULL)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey('UserProfile', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=40)  # New , Contacted , Converted , Unconverted
    organization = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
