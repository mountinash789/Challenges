from django.apps import apps
from django.test import TestCase
from backend.apps import BackendConfig
from frontend.apps import FrontendConfig


class AppsConfigTest(TestCase):
    def test_app_backend(self):
        self.assertEqual(BackendConfig.name, 'backend')
        self.assertEqual(apps.get_app_config('backend').name, 'backend')

    def test_app_frontend(self):
        self.assertEqual(FrontendConfig.name, 'frontend')
        self.assertEqual(apps.get_app_config('frontend').name, 'frontend')
