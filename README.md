# netbox-build-network

Adds a top-level NetBox menu item ("Build Network"). Clicking it hits an internal
plugin URL, which 302-redirects the browser to:

    http://drone.as49206.net:8080/?message=<username>-<timestamp>

so the browser itself performs the final GET request.

## Install

### Standard (bare-metal / venv) install

On the NetBox host, activate NetBox's virtualenv and install the plugin
straight from GitHub:

```bash
source /opt/netbox/venv/bin/activate
pip install git+https://github.com/wvandervaart/netbox-build-network.git
```

To pin a specific commit/tag instead of tracking `master`:

```bash
pip install git+https://github.com/wvandervaart/netbox-build-network.git@<tag-or-commit>
```

In NetBox's `configuration.py` (typically `/opt/netbox/netbox/netbox/configuration.py`),
add the plugin:

```python
PLUGINS = [
    'netbox_build_network',
]
```

Run NetBox's standard upgrade step and restart the services:

```bash
cd /opt/netbox
sudo ./upgrade.sh          # or: python manage.py migrate / collectstatic
sudo systemctl restart netbox netbox-rq
```

### NetBox Docker install

Add the package to your `plugin_requirements.txt`:

```
git+https://github.com/wvandervaart/netbox-build-network.git
```

Enable it in `configuration/plugins.py`:

```python
PLUGINS = [
    'netbox_build_network',
]
```

Rebuild the image and restart the stack:

```bash
docker compose build --no-cache
docker compose up -d
```

### Verify

Log in to NetBox, and confirm a "Build Network" entry appears in the top
navigation menu. Clicking it should redirect your browser to
`drone.as49206.net:8080` with a `message` query parameter.

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