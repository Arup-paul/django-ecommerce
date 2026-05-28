from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.tokens import email_verification_token


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
