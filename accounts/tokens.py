from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """One-time token for verifying a user's email.

    Hashing in the user's pk, timestamp, and is_verified flag means the token
    becomes invalid automatically once the account is verified.
    """

    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_verified}"


email_verification_token = EmailVerificationTokenGenerator()


# Stock PasswordResetTokenGenerator already hashes in the user's password hash
# and last_login, so a reset token auto-invalidates once the password changes
# (or the user logs in). No subclass needed — we just want our own instance.
password_reset_token = PasswordResetTokenGenerator()
