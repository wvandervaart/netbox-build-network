from urllib.parse import urlencode

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.utils.html import escape
from django.views import View
from netbox.plugins.utils import get_plugin_config

_PAGE_TEMPLATE = """<!DOCTYPE html>
<html>
<head><title>Build Network</title></head>
<body>
<p><a href="{buildnw_url}" target="_blank" rel="noopener noreferrer">Send buildnw request</a></p>
</body>
</html>
"""


class BuildnwRedirectView(PermissionRequiredMixin, View):
    """Presents a link that opens the configured buildnw_url in a new tab with message=<user>."""

    permission_required = 'netbox_build_network.send_buildnw'

    def get(self, request):
        base_url = get_plugin_config('netbox_build_network', 'buildnw_url')
        message = request.user.get_username()
        query = urlencode({'message': message})
        buildnw_url = f'{base_url}?{query}'

        html = _PAGE_TEMPLATE.format(buildnw_url=escape(buildnw_url))
        return HttpResponse(html)
