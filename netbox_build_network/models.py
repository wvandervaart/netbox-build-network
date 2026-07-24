from django.db import models


class BeaconPermissions(models.Model):
    """Unmanaged model that exists solely to register a custom permission."""

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ('send_beacon', 'Can send beacon'),
        )
