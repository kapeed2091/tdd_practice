from django.apps import AppConfig


class WalletV2AppConfig(AppConfig):
    name = "wallet_v2"

    def ready(self):
        from wallet_v2 import signals # pylint: disable=unused-variable
