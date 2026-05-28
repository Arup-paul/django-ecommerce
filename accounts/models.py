import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Manager for the custom User model where email is the unique identifier."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("Users must have an email address"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model: UUID primary key, email-based login, no username."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    name = models.CharField(_("full name"), max_length=255, blank=True)

    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    is_verified = models.BooleanField(_("email verified"), default=False)

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name or self.email

    def get_short_name(self):
        return self.name.split(" ")[0] if self.name else self.email


class UserProfile(models.Model):
    """Extra, optional info that doesn't belong on the auth User row itself.

    Kept separate from User so the auth table stays lean and so we can grow
    profile fields without touching the login-critical model.
    """

    # OneToOneField = exactly one profile per user. CASCADE: delete the profile
    # if the user is deleted. related_name lets us write `user.profile`.
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="profile",
    )
    phone = models.CharField(_("phone number"), max_length=20, blank=True)
    avatar = models.ImageField(_("avatar"), upload_to="avatars/", blank=True, null=True)
    bio = models.TextField(_("bio"), max_length=500, blank=True)
    date_of_birth = models.DateField(_("date of birth"), blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")

    def __str__(self):
        return f"Profile of {self.user.email}"


class Address(models.Model):
    """A shipping/billing address. A user can have many (multi-address)."""

    class AddressType(models.TextChoices):
        # TextChoices = enum stored as text. First value = DB value, second = label.
        HOME = "home", _("Home")
        WORK = "work", _("Work")
        OTHER = "other", _("Other")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="addresses",
    )

    full_name = models.CharField(_("full name"), max_length=255)
    phone = models.CharField(_("phone number"), max_length=20)
    line1 = models.CharField(_("address line 1"), max_length=255)
    line2 = models.CharField(_("address line 2"), max_length=255, blank=True)
    city = models.CharField(_("city"), max_length=100)
    state = models.CharField(_("state"), max_length=100)
    postal_code = models.CharField(_("postal code"), max_length=20)
    country = models.CharField(_("country"), max_length=100, default="India")

    address_type = models.CharField(
        _("address type"),
        max_length=10,
        choices=AddressType.choices,
        default=AddressType.HOME,
    )
    is_default = models.BooleanField(_("default address"), default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("address")
        verbose_name_plural = _("addresses")
        # Default address first, then newest. Used wherever we list addresses.
        ordering = ["-is_default", "-created_at"]

    def __str__(self):
        return f"{self.full_name}, {self.city} ({self.user.email})"

    def save(self, *args, **kwargs):
        # Enforce "only one default per user": if this one is being set as
        # default, unset the flag on all the user's other addresses first.
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(
                is_default=False
            )
        super().save(*args, **kwargs)
