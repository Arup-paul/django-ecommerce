from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.tokens import email_verification_token, password_reset_token


def _print_dev_link(label, url):
    """In DEBUG, echo the raw link to the terminal on its own line.

    Email bodies are quoted-printable encoded and soft-wrap at 76 chars, which
    splits long verify/reset URLs across two lines and breaks copy-paste. This
    prints the URL unencoded so it's always one clean, clickable line.
    """
    if settings.DEBUG:
        print(f"\n[DEV] {label}:\n{url}\n", flush=True)


def send_verification_email(user):
    """Build a signed verify link and email it to the user."""
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    path = reverse("accounts:verify_email", kwargs={"uidb64": uid, "token": token})
    verify_url = f"{settings.SITE_URL}{path}"

    subject = "Verify your ShopDjango email"
    message = (
        f"Hi {user.get_short_name()},\n\n"
        f"Thanks for signing up. Please verify your email by clicking the link below:\n\n"
        f"{verify_url}\n\n"
        f"If you didn't create this account, you can ignore this email."
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    _print_dev_link("Email verification link", verify_url)


def send_password_reset_email(user):
    """Build a signed password-reset link and email it to the user."""
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = password_reset_token.make_token(user)
    path = reverse("accounts:password_reset_confirm", kwargs={"uidb64": uid, "token": token})
    reset_url = f"{settings.SITE_URL}{path}"

    subject = "Reset your ShopDjango password"
    message = (
        f"Hi {user.get_short_name()},\n\n"
        f"We received a request to reset your password. Click the link below to choose a new one:\n\n"
        f"{reset_url}\n\n"
        f"This link can only be used once and expires shortly. "
        f"If you didn't request a reset, you can safely ignore this email."
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
    _print_dev_link("Password reset link", reset_url)
