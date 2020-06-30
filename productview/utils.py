"""Basic utilities used in the product view application"""

import uuid
import os

from django.core.files.storage import default_storage

from productview.models import Upload, WebHook, Event
from productview import tasks


def save_csv(products_file):
    """Saves products csv file to local file system"""

    file_name = "{}.csv".format(uuid.uuid4())
    file_path = os.path.join("uploads", file_name)
    file_path = default_storage.save(file_path, products_file)

    upload_object = Upload.objects.create(
        file_name=products_file.name, size=products_file.size,
        file_path=file_path
    )

    tasks.parse_products_from_file.delay(upload_object.id)

    return upload_object.id


def gen_chunks(reader, chunksize=100):
    """
    Chunk generator. Take a CSV `reader` and yield
    `chunksize` sized slices.
    """
    chunk = []
    for index, line in enumerate(reader):
        if (index % chunksize == 0 and index > 0):
            yield chunk
            del chunk[:]
        chunk.append(line)
    yield chunk


def notify_hooks(event_code, product_object):
    """Notifies all webhooks about event"""

    hooks = WebHook.objects.filter(event__code=event_code)
    event_obj = Event.objects.get(code=event_code)
    payload = {
        "product_id": product_object.id,
        "SKU": product_object.sku,
        "Name": product_object.name,
        "Description": product_object.description,
        "event": event_obj.name
    }
    for hook in hooks:
        tasks.send_payload_url.delay(hook.url, payload)
