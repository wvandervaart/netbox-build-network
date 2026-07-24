# netbox-build-network

Adds a top-level NetBox menu item ("Send Beacon"). Clicking it hits an internal
plugin URL, which 302-redirects the browser to:

    http://drone.as49206.net:8080/?message=<username>-<timestamp>

so the browser itself performs the final GET request.

## Install

From the NetBox virtualenv:

```bash
pip install -e /Users/wouter/Documents/git/MenuPlugin
```

In NetBox's `configuration.py`, add the plugin:

```python
PLUGINS = [
    'netbox_build_network',
]
```

Then restart NetBox (and any WSGI/RQ workers):

```bash
python manage.py migrate   # no-op, no models, but harmless to run
sudo systemctl restart netbox netbox-rq
```

## Compatibility note

This uses `netbox.plugins` for `PluginConfig` / `PluginMenuItem`, which is the
import path on NetBox >= 3.5. On older NetBox versions, change the imports in
`__init__.py` and `navigation.py` to `extras.plugins` instead.

## Notes

- The menu item requires login (`LoginRequiredMixin`) since NetBox already
  requires auth for the UI.
- Timestamp is UTC, ISO 8601 (`YYYY-MM-DDTHH:MM:SSZ`).
- If `drone.as49206.net` is unreachable from the end user's browser (rather
  than the NetBox server), the redirect will fail client-side — this plugin
  does not proxy the request server-side.