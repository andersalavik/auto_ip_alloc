# netbox/auto_ip_alloc/plugin.py

from extras.plugins import PluginConfig

class AutoIPAllocConfig(PluginConfig):
    name = 'auto_ip_alloc'
    verbose_name = 'Auto IP Allocation Plugin'
    description = 'Automatically allocate IP addresses from prefixes via REST API'
    version = '0.1'
    author = 'Your Name'
    author_email = 'your.email@example.com'
    base_url = 'auto-ip-alloc'
    required_settings = []
    default_settings = {}

    def ready(self):
        super().ready()
        from .api import urls as api_urls
        self.api_urlpatterns = api_urls.urlpatterns

config = AutoIPAllocConfig
