import json
from urllib.error import URLError
from urllib.request import Request, urlopen

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.views import View
from netbox.plugins.utils import get_plugin_config


class BuildnwRedirectView(PermissionRequiredMixin, View):
    """Sends a server-side authenticated POST to the configured buildnw_url."""

    permission_required = 'netbox_build_network.send_buildnw'

    def get(self, request):
        base_url = get_plugin_config('netbox_build_network', 'buildnw_url')
        token = get_plugin_config('netbox_build_network', 'buildnw_token')
        message = request.user.get_username()
        back_url = request.META.get('HTTP_REFERER') or '/'

        body = json.dumps({'message': message}).encode('utf-8')
        req = Request(
            base_url,
            data=body,
            method='POST',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}',
            },
        )

        try:
            urlopen(req, timeout=10)
        except URLError as exc:
            messages.error(request, f'Failed to send buildnw request: {exc}')
        else:
            messages.success(request, 'Buildnw request sent.')

        return redirect(back_url)