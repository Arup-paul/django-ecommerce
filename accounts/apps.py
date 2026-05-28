from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        # Importing here (inside ready) registers the @receiver handlers once
        # the app registry is loaded. Importing at module top would risk
        # circular imports. noqa: the import is for its side effects.
        import accounts.signals  # noqa: F401
