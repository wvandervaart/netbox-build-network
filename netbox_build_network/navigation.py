from netbox.plugins import PluginMenuItem

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_build_network:build_network',
        link_text='Build Network',
        permissions=['netbox_build_network.send_buildnw'],
    ),
)