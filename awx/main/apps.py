from django.apps import AppConfig
from django.core.cache import cache
from django.core.signals import setting_changed
from django.utils.translation import gettext_lazy as _

from awx.conf import settings_registry


def setting_clear_cache_callback(sender, **kwargs):
    if 'setting' not in kwargs:
        return

    setting_key = kwargs['setting']
    key_list = [setting_key]
    for dependent_key in settings_registry.get_dependent_settings(setting_key):
        key_list.append(dependent_key)
    cache_keys = set(key_list)
    cache.delete_many(cache_keys)


class MainConfig(AppConfig):
    name = 'awx.main'
    verbose_name = _('Main')

    def ready(self):
        setting_changed.connect(setting_clear_cache_callback)
