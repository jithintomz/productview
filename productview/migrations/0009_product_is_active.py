# Generated by Django 2.2.2 on 2019-07-02 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productview', '0008_auto_20190702_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.IntegerField(default=1),
        ),
    ]
