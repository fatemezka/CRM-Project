from django.db.models.signals import post_save  # when the user actually created in the database
from .models import *


def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# when the object of User model created this signal will run
# (and run this post_user_created_signal function after receiving this signal)
post_save.connect(post_user_created_signal, sender=User)
