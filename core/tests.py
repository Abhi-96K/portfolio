from django.test import TestCase
from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import user_logged_in


class SignalDisconnectionTest(TestCase):
    def test_update_last_login_disconnected(self):
        # Retrieve all active receivers for user_logged_in signal
        receivers = [r[1]() for r in user_logged_in.receivers if r[1]() is not None]
        # Assert update_last_login is not in the active receivers
        self.assertNotIn(update_last_login, receivers)

