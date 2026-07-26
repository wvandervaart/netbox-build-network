# netbox-build-network

Adds a "Build Network" entry under the **Plugins** dropdown in NetBox's top
nav. Clicking it hits an internal plugin URL, which triggers a server-side
authenticated `POST` to a configurable `buildnw_url` (default
`http://example.com:8080/`), with the current username as a JSON body, e.g.:

```bash
curl -X POST http://example.com:8080/ \
    -H "Authorization: Bearer <buildnw_token>" \
    -H "Content-Type: application/json" \
    -d '{"message": "<username>"}'
```

The NetBox server makes this request itself (not the end user's browser), so
the target only needs to be reachable from the NetBox host, and the user is
redirected back to the page they came from with a success/failure message.

## Configuration

The buildnw target and credentials are set via NetBox's `PLUGINS_CONFIG`, not
hardcoded. Add this to `configuration.py` (or `configuration/plugins.py` for
Docker):

```python
PLUGINS_CONFIG = {
    'netbox_build_network': {
        'buildnw_url': 'http://example.com:8080/',
        'buildnw_token': 'changeme123',
    },
}
```

`buildnw_token` is sent as an `Authorization: Bearer <token>` header on every
request. If `buildnw_url` is omitted, it falls back to the plugin's
`default_settings['buildnw_url']` in `netbox_build_network/__init__.py`,
which also points at `http://example.com:8080/`; `buildnw_token` falls back
to an empty string, which will fail authentication against most real
buildnw endpoints — set it explicitly.

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
and confirm a "Build Network" entry appears. Clicking it should send a POST
request to your configured `buildnw_url` and redirect you back to the page
you came from with a success or failure banner.

## Compatibility note

This uses `netbox.plugins` for `PluginConfig` / `PluginMenuItem`, which is the
import path on NetBox >= 3.5. On older NetBox versions, change the imports in
`__init__.py` and `navigation.py` to `extras.plugins` instead.

## Notes

- The menu item and view require the `netbox_build_network.send_buildnw`
  permission (see **Permissions** above), which implies being logged in.
- The request is made by the NetBox server itself, so `buildnw_url` must be
  reachable from the NetBox host, not from end users' browsers.
- The request has a 10-second timeout; failures (unreachable host, non-2xx
  response, timeout) are reported back to the user via a Django messages
  banner rather than raising an error page.