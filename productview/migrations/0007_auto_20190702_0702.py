# Generated by Django 2.2.2 on 2019-07-02 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productview', '0006_auto_20190702_0657'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WebHooks',
            new_name='WebHook',
        ),
    ]
