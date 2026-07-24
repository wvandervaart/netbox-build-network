from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='BuildnwPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'managed': False,
                'default_permissions': (),
                'permissions': [('send_buildnw', 'Can send buildnw')],
            },
        ),
    ]
