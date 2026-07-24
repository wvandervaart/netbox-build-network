from django.db import migrations


def delete_stale_permission(apps, schema_editor):
    """Removes the old send_buildnw auth.Permission row left behind by the rename below."""
    Permission = apps.get_model('auth', 'Permission')
    Permission.objects.filter(
        content_type__app_label='netbox_build_network',
        codename='send_buildnw',
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_build_network', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(old_name='BuildnwPermissions', new_name='Buildnw'),
        migrations.AlterModelOptions(
            name='buildnw',
            options={
                'managed': False,
                'default_permissions': (),
                'permissions': [('send', 'Can send buildnw')],
            },
        ),
        migrations.RunPython(delete_stale_permission, migrations.RunPython.noop),
    ]
