from django.apps import AppConfig
import logging
from edx_django_utils.plugins import PluginSettings, PluginURLs, plugin_settings
# rom opefnedx.core.djangoapps.plugins.constants import ProjectType
# from openedx.core.djangoapps.plugins.constants import (
#     ProjectType,
    
# )
log = logging.getLogger(__name__)

class GreetingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'greetings_plugin'

    plugin_app = {
        PluginURLs.CONFIG: {
            'lms.djangoapp': {
                PluginURLs.NAMESPACE: name,
                PluginURLs.REGEX: "^api/greetings/",
                PluginURLs.RELATIVE_PATH: "urls",
            },
        
           'cms.djangoapp': {
                PluginURLs.NAMESPACE: name,
                PluginURLs.REGEX: "^api/greetings/",
                PluginURLs.RELATIVE_PATH: "urls",
            }
        },
        PluginSettings.CONFIG: {
            'lms.djangoapp': {
               # Configure each settings, as needed.
                'production': {

                    # The python path (relative to this app) to the settings module for the relevant Project Type and Settings Type.
                    # Optional; Defaults to 'settings'.
                    PluginSettings.RELATIVE_PATH: 'settings.production',
                },
                'common': {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
            },
            'cms.djangoapp': {
               # Configure each settings, as needed.
                'production': {

                    # The python path (relative to this app) to the settings module for the relevant Project Type and Settings Type.
                    # Optional; Defaults to 'settings'.
                    PluginSettings.RELATIVE_PATH: 'settings.production',
                },
                'common': {
                    PluginSettings.RELATIVE_PATH: 'settings.common',
                },
            }
        },
        
    }

    def ready(self):
        log.info("{label} is ready.".format(label=self.label))