from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to="pics/")


class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Chat(models.Model):
    name = models.CharField(max_length=100)
    ava = models.ImageField(upload_to='avatars/', null=True)
    members = models.ManyToManyField(User, blank=True)
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)

class Message(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
