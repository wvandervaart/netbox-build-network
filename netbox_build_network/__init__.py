from netbox.plugins import PluginConfig


class BuildNetworkConfig(PluginConfig):
    name = 'netbox_build_network'
    verbose_name = 'Build Network'
    description = 'Adds a menu item that sends an authenticated POST request to a buildnw URL'
    version = '0.1.1'
    base_url = 'build-network'
    author = 'wouter'
    default_settings = {
        'buildnw_url': 'http://example.com:8080/',
        'buildnw_token': '',
    }


config = BuildNetworkConfig