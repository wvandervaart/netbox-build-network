from netbox.plugins import PluginConfig


class BuildNetworkConfig(PluginConfig):
    name = 'netbox_build_network'
    verbose_name = 'Build Network'
    description = 'Adds a menu item that sends a GET request to a beacon URL'
    version = '0.1.0'
    base_url = 'build-network'
    author = 'wouter'
    default_settings = {
        'beacon_url': 'http://example.com:8080/',
    }


config = BuildNetworkConfig