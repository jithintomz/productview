#Database models for the productview application

from datetime import datetime

from django.db import models
from psqlextra.manager import PostgresManager


class Upload(models.Model):
    """Model that saves uploaded file"""

    file_name = models.CharField(max_length=250)
    uploaded_time = models.DateTimeField(default=datetime.now)
    size = models.IntegerField()
    file_path = models.CharField(max_length=500, null=True, blank=True)
    # {1:Yet to begin, 2:Failiure,3:Success}
    processing_status = models.IntegerField(default=1)


class Product(models.Model):
    name = models.CharField(max_length=250)
    sku = models.CharField(max_length=250, unique=True, db_index=True)
    description = models.TextField(null=True)
    is_active = models.IntegerField(default=1)  # {1:active, 2:inactive}
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE, null=True)
    created_time = models.DateTimeField(default=datetime.now)
    updated_time = models.DateTimeField(default=datetime.now)
    objects = PostgresManager()


class Event(models.Model):
    """Individual events used for hooks"""
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100, unique=True)


class WebHook(models.Model):
    """Tracks webhooks added by the user"""
    
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=1000)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
