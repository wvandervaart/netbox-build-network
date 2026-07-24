from django.db import models


class BuildnwPermissions(models.Model):
    """Unmanaged model that exists solely to register a custom permission."""

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ('send_buildnw', 'Can send buildnw'),
        )
