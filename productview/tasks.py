"""Defines a set of asynchronous tasks used throught the app"""

import csv

import requests
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.files.storage import default_storage

from acme.celery import app
from productview import utils
from productview.models import Upload, Product


@shared_task
def parse_products_from_file(upload_id):
    """
    Parses csv file and adds products to the
    database
    """

    upload_obj = Upload.objects.get(id=upload_id)
    csv_reader = csv.reader(
        default_storage.open(upload_obj.file_path, 'r+')
    )
    header_row = next(csv_reader)
    header_row = [value.lower() for value in header_row]
    headers = ["name", "sku", "description"]

    if set(header_row) != set(headers):
        upload_obj.processing_status = 1
        upload_obj.save()
        return {"status": "Failed", "message": "Invalid csv format"}

    channel_layer = get_channel_layer()
    channel_name = "upload_{}".format(upload_id)
    records_saved = 0
    chunksize = 20000
    async_to_sync(channel_layer.group_send)(
        channel_name,
        {
            'type': 'upload_message',
            "message": "Saving Products to Database",
            "saved_records": records_saved,
            "status": "inprogress"
        }
    )

    for chunk in utils.gen_chunks(csv_reader, chunksize=chunksize):
        products = {}
        async_to_sync(channel_layer.group_send)(
            channel_name,
            {
                'type': 'upload_message',
                "message": "Saving Products to Database",
                "saved_records": records_saved,
                "status": "inprogress"
            }
        )

        for row in chunk:
            sku = row[1].lower()
            product = dict(
                name=row[0], sku=sku,
                description=row[2], upload_id=upload_id
            )
            products[sku] = product
        Product.objects.bulk_upsert(["sku"], products.values())
        records_saved += chunksize

    upload_obj.processing_status = 2
    upload_obj.save()
    default_storage.delete(upload_obj.file_path)
    async_to_sync(channel_layer.group_send)(
        channel_name,
        {
            'type': 'upload_message',
            "message": "Products saved successfully",
            "status": "success",
            "saved_records": records_saved
        }
    )
    return {"status": "Success"}


@app.task(
    bind=True,
    autoretry_for=(requests.exceptions.RequestException,),
    retry_kwargs={'max_retries': 3, 'countdown': 300}
)
def send_payload_url(self, url, payload):
    requests.post(url, data=payload)
