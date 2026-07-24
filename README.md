# netbox-build-network

Adds a "Build Network" entry under the **Plugins** dropdown in NetBox's top
nav. Clicking it hits an internal plugin URL, which opens a new browser tab
pointed at a configurable `buildnw_url` (default `http://example.com:8080/`),
appending `?message=<username>`, e.g.:

    http://example.com:8080/?message=<username>

so the new tab performs the GET request while the original NetBox tab stays
where it was.

## Configuration

The buildnw target is set via NetBox's `PLUGINS_CONFIG`, not hardcoded. Add
this to `configuration.py` (or `configuration/plugins.py` for Docker):

```python
PLUGINS_CONFIG = {
    'netbox_build_network': {
        'buildnw_url': 'http://example.com:8080/',
    },
}
```

If omitted, it falls back to the plugin's `default_settings['buildnw_url']`
in `netbox_build_network/__init__.py`, which also points at
`http://example.com:8080/`.

## Permissions

Access is gated by a custom permission, `netbox_build_network.send_buildnw`,
defined on an unmanaged model (`Buildnw`) that exists purely to register it —
this plugin has no real data model. Both the menu item and the underlying
view check it:

- Users without the permission don't see "Build Network" in the **Plugins**
  menu at all.
- Hitting the URL directly without the permission returns a 403; without
  being logged in, it redirects to the login page.
- Superusers always pass, per normal Django behavior.

Grant it the same way as any other NetBox permission: **Admin → Permissions**
(NetBox's own Permissions page, not the Django admin's raw per-user
permission checkbox — NetBox's auth backend doesn't consult that). Create or
edit a Permission entry:

- **Object types**: `netbox_build_network | buildnw`
- **Actions**: check `send` ("Can send buildnw")
- **Enabled**: checked
- **Users**/**Groups**: assign directly to a user, or to a group — if a
  group, the target user must actually be a member of it

If you installed before this permission's model/action were renamed
(`0002_rename_buildnw_action`), run `migrate` again after upgrading, then
edit your existing Permission entry: the **Object type** carries over
automatically (Django renames the underlying `ContentType` row in place),
but you must manually uncheck the old `send_buildnw` action and check the
new `send` action — that field is a plain list of strings and isn't
rewritten by the migration.

NetBox constructs the granted permission string as
`{app_label}.{action}_{model_name}` (see
`netbox/netbox/authentication/__init__.py` in NetBox core), which is why the
model is named `Buildnw` and the action `send` — combined they produce
`netbox_build_network.send_buildnw`, matching what the plugin checks for.

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
sudo ./upgrade.sh          # runs migrate + collectstatic; needed to register the plugin's permission
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

Log in to NetBox, open the **Plugins** dropdown in the top navigation menu,
and confirm a "Build Network" entry appears. Clicking it should open a new
tab pointed at your configured `buildnw_url` with a `message` query parameter,
while the original NetBox tab stays put.

## Compatibility note

This uses `netbox.plugins` for `PluginConfig` / `PluginMenuItem`, which is the
import path on NetBox >= 3.5. On older NetBox versions, change the imports in
`__init__.py` and `navigation.py` to `extras.plugins` instead.

## Notes

- The menu item and view require the `netbox_build_network.send_buildnw`
  permission (see **Permissions** above), which implies being logged in.
- If the configured `buildnw_url` host is unreachable from the end user's
  browser (rather than the NetBox server), the request will fail
  client-side — this plugin does not proxy the request server-side.
- The new-tab open relies on an inline `<script>` in the intermediate page;
  a strict `Content-Security-Policy` (e.g. one blocking `script-src` inline)
  in front of NetBox would prevent it from firing.