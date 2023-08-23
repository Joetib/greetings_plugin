from django.apps import AppConfig
from edx_django_utils.plugins import PluginSettings, PluginURLs, plugin_apps
from openedx.core.djangoapps.plugins.constants import ProjectType
# from openedx.core.djangoapps.plugins.constants import (
#     ProjectType,
    
# )

class GreetingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'greetings_plugin'

    plugin_app = {
        PluginURLs.CONFIG: {
            'lms.djangoapp': {
                PluginURLs.NAMESPACE: name,
                PluginURLs.REGEX: "^greetings/",
                PluginURLs.RELATIVE_PATH: "urls",
            }
        },
        PluginURLs.CONFIG: {
           'cms.djangoapp': {
                PluginURLs.NAMESPACE: name,
                PluginURLs.REGEX: "^greetings/",
                PluginURLs.RELATIVE_PATH: "urls",
            }
        },
        # PluginSettings.CONFIG: {
        #     ProjectType.LMS: {
        #         SettingsType.COMMON: {PluginSettings.RELATIVE_PATH: "settings.common"},
        #     }
        # },
        
    }