"""
Created on 14/05/18

@author: revanth
"""
from django_swagger_utils.drf_server.utils.server_gen.custom_api_test_case import \
    CustomAPITestCase

import mock

from ib_gamification_validation.utils.user.gas_auth_service_interface_mock\
    import GasAuthServiceInterfaceMock
from ib_gamification_validation.utils.user.gas_profile_service_interface_mock import \
        GasProfileServiceInterfaceMock


def test_case_decorator(func):
    def wrapped(*args, **kwargs):
        import os
        pid = os.getpid()
        db_number = (pid % 10) + 1
        from django.conf import settings
        setattr(settings, 'REDIS_LEADERBOARD_DB', db_number)
        print args[0].__class__.__name__, func.__name__
        print 'REDIS_DB_NAME', settings.REDIS_LEADERBOARD_DB

        os.system(
            'cp ~/dynamodb/shared-local-instance.db.backup '
            '~/dynamodb/shared-local-instance.db')

        from ib_gamification_validation.mocks.ibc_billing_client_adapter_mock \
            import IBCBillingClientAdapterMock
        from ib_gamification_validation.mocks.ibc_slots_client_adapter_mock \
            import IBCSlotsClientAdapterMock
        from ib_gamification_validation.mocks.\
            customer_analytics_client_adapter_mock import \
            CustomerAnalyticsClientAdapterMock
        from ib_gamification_validation.utils.gd_mock_class import GDMockClass
        from ib_gamification_validation.mocks.\
            ibc_payments_wallet_client_adapter_mock import \
            IBCPaymentsWalletClientAdapterMock

        with mock.patch("gas_profile.interfaces.gas_profile_service_interface."
                        "GasProfileServiceInterface",
                        GasProfileServiceInterfaceMock), \
             mock.patch("gas_profile.interfaces."
                        "extended_gas_profile_service_interface."
                        "ExtendedGasProfileServiceInterface",
                        GasProfileServiceInterfaceMock), \
             mock.patch("gas_auth.interfaces."
                        "extended_gas_auth_service_interface."
                        "ExtendedGasAuthServiceInterface",
                        GasAuthServiceInterfaceMock), \
             mock.patch("ib_gamification_backend.service_adapters."
                        "ibc_billing_client_adapter.IBCBillingClientAdapter",
                        IBCBillingClientAdapterMock), \
             mock.patch("ib_gamification_backend.service_adapters."
                        "customer_analytics_client_adapter."
                        "CustomerAnalyticsClientAdapter",
                        CustomerAnalyticsClientAdapterMock), \
             mock.patch("ib_gamification_backend.service_adapters."
                        "ibc_slots_client_adapter.IBCSlotsClientAdapter",
                        IBCSlotsClientAdapterMock), \
             mock.patch("ib_gamification_backend.service_adapters."
                        "game_developer_adapter.GameDeveloperAdapter",
                        GDMockClass), \
             mock.patch("ib_gamification_backend.service_adapters."
                        "ibc_payments_wallet_client_adapter."
                        "IBCPaymentsWalletClientAdapter",
                        IBCPaymentsWalletClientAdapterMock):

            return func(*args, **kwargs)

    return wrapped


class CustomAPITestCaseWrapper(CustomAPITestCase):
    def __init__(self, *args, **kwargs):
        super(CustomAPITestCaseWrapper, self).__init__(*args, **kwargs)

        for attr, val in self.__class__.__dict__.items():
            if callable(val):
                if attr.startswith('test_case') \
                        and val.__name__.startswith('test_case'):
                    setattr(self.__class__, attr, test_case_decorator(val))

    def test_case(self):
        return super(CustomAPITestCaseWrapper, self).test_case()

    def tearDown(self):
        import redis
        from django.conf import settings
        conn = redis.StrictRedis(
            host=settings.REDIS_HOST, port=settings.REDIS_PORT,
            db=settings.REDIS_LEADERBOARD_DB)
        conn.flushdb()
        # from ib_game_object.dynamo_db_models import UserGameObject,
        # UserDeck, UserUnassignedGameObject
        # models = [UserGameObject, UserDeck, UserUnassignedGameObject]
        # from ib_content_portal.populate.load_tables import drop_tables, \
        #     load_tables
        # drop_tables(models)
        # load_tables(models)
