# Generated by Django 2.2.2 on 2019-06-30 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productview', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='file_path',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
