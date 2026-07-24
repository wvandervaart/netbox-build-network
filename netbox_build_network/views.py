import json
from urllib.parse import urlencode

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.views import View
from netbox.plugins.utils import get_plugin_config

_PAGE_TEMPLATE = """<!DOCTYPE html>
<html>
<head><title>Sending buildnw&hellip;</title></head>
<body>
<script>
  window.open({buildnw_url}, '_blank', 'noopener,noreferrer');
  window.location.replace({back_url});
</script>
<p>Buildnw sent in a new window.</p>
</body>
</html>
"""


class BuildnwRedirectView(PermissionRequiredMixin, View):
    """Opens the configured buildnw_url in a new tab, triggering a GET with message=<user>."""

    permission_required = 'netbox_build_network.send_buildnw'

    def get(self, request):
        base_url = get_plugin_config('netbox_build_network', 'buildnw_url')
        message = request.user.get_username()
        query = urlencode({'message': message})
        buildnw_url = f'{base_url}?{query}'
        back_url = request.META.get('HTTP_REFERER') or '/'

        html = _PAGE_TEMPLATE.format(
            buildnw_url=json.dumps(buildnw_url),
            back_url=json.dumps(back_url),
        )
        return HttpResponse(html)
