from datetime import datetime

from django.db import models
from psqlextra.manager import PostgresManager



class Upload(models.Model):
    """Model that saves uploaded file"""

    file_name = models.CharField(max_length=250)
    uploaded_time = models.DateTimeField(default=datetime.now)
    size = models.IntegerField()
    file_path = models.CharField(max_length=500, null=True, blank=True)
    processing_status = models.IntegerField(default=1)


class Product(models.Model):
    name = models.CharField(max_length=250)
    sku = models.CharField(max_length=250, unique=True)
    description = models.TextField(null=True)
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    created_time = models.DateTimeField(default=datetime.now)
    updated_time = models.DateTimeField(default=datetime.now)
    objects = PostgresManager()

    