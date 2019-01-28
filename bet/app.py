from django.apps import AppConfig


class BetAppConfig(AppConfig):
    name = "bet"

    def ready(self):
        from bet import signals # pylint: disable=unused-variable
