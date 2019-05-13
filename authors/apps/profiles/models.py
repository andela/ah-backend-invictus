from django.db import models
from authors.apps.authentication.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserProfile(models.Model):
    """A model that contains different fields."""

    user = models.OneToOneField(User, to_field="username", on_delete=models.CASCADE)
    image = models.URLField(blank=True)
    bio = models.TextField(blank=True, max_length=200)
    firstname = models.CharField(blank=True, max_length=25)
    lastname = models.CharField(blank=True, max_length=25)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Method to return the string representation of an object."""
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Follow(models.Model):
    follower = models.ForeignKey(User,
                                 related_name="follower",
                                 on_delete=models.CASCADE,
                                 default=False)
    followed = models.ForeignKey(User, related_name="followed",
                                 on_delete=models.CASCADE,
                                 default=False)
