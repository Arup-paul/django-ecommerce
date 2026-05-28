from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import UserProfile


# @receiver wires this function to the post_save signal of the User model.
# sender=User means "only fire for User saves", not every model.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """Whenever a brand-new User row is saved, give it a blank profile.

    `created` is True only on INSERT (first save), so we don't recreate the
    profile on every update. get_or_create is a safety net for users that
    predate this signal.
    """
    if created:
        UserProfile.objects.get_or_create(user=instance)
