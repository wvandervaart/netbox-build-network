from datetime import datetime, timezone
from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import View

BEACON_URL = 'http://drone.as49206.net:8080/'


class BeaconRedirectView(LoginRequiredMixin, View):
    """Redirects the browser to BEACON_URL, triggering a GET with message=<user>-<timestamp>."""

    def get(self, request):
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        message = f'{request.user.get_username()}-{timestamp}'
        query = urlencode({'message': message})
        return HttpResponseRedirect(f'{BEACON_URL}?{query}')