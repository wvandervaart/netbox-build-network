from django.db import models


class Buildnw(models.Model):
    """Unmanaged model that exists solely to register a custom permission.

    NetBox's ObjectPermission backend builds granted permission strings as
    f"{app_label}.{action}_{model_name}" (see netbox.authentication), so the
    model name and action are chosen together to produce
    netbox_build_network.send_buildnw.
    """

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ('send', 'Can send buildnw'),
        )
