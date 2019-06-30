import csv
import json

from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from productview import utils, tasks
from productview.models import *


@shared_task
def parse_products_from_file(upload_id):
    """Parses csv file and adds products to the
    database"""

    upload_obj = Upload.objects.get(id=upload_id)
    csv_reader = csv.reader(open(upload_obj.file_path, "r+"))
    header_row = next(csv_reader)
    header_row = [value.lower() for value in header_row]
    headers = ["name", "sku", "description"]
    if set(header_row) != set(headers):
        upload_obj.processing_status = 1
        upload_obj.save()
        return {"status": "Failed", "message": "Invalid csv format"}
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("upload_{}".format(
        upload_id), {'type': 'upload_message', "message": "Saving to Database"})
    for chunk in utils.gen_chunks(csv_reader, chunksize=20000):
        products = {}
        
        for row in chunk:
            sku = row[1].lower()
            product = dict(name=row[0], sku=sku, description=row[2], upload_id=upload_id)
            products[sku] = product

        Product.objects.bulk_upsert(["sku"],products.values())

    return {"status": "Success"}

@shared_task
def sender():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)("test", {"k": "k"})
