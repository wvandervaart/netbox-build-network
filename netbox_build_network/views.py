import json
from datetime import datetime, timezone
from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View

BEACON_URL = 'http://drone.as49206.net:8080/'

_PAGE_TEMPLATE = """<!DOCTYPE html>
<html>
<head><title>Sending beacon&hellip;</title></head>
<body>
<script>
  window.open({beacon_url}, '_blank', 'noopener,noreferrer');
  window.location.replace({back_url});
</script>
<p>Beacon sent in a new window.</p>
</body>
</html>
"""


class BeaconRedirectView(LoginRequiredMixin, View):
    """Opens BEACON_URL in a new tab, triggering a GET with message=<user>-<timestamp>."""

    def get(self, request):
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        message = f'{request.user.get_username()}-{timestamp}'
        query = urlencode({'message': message})
        beacon_url = f'{BEACON_URL}?{query}'
        back_url = request.META.get('HTTP_REFERER') or '/'

        html = _PAGE_TEMPLATE.format(
            beacon_url=json.dumps(beacon_url),
            back_url=json.dumps(back_url),
        )
        return HttpResponse(html)