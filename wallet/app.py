from django.apps import AppConfig


class WalletAppConfig(AppConfig):
    name = "wallet"

    def ready(self):
        from wallet import signals # pylint: disable=unused-variable
