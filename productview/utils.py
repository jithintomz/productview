import uuid

from django.core.files.storage import default_storage

from productview.models import *
from productview import tasks


def save_csv(products_file):
    """Saves products csv file to local file system"""

    file_name = "{}.csv".format(uuid.uuid4())
    file_path = default_storage.save(file_name, products_file)

    upload_object = Upload.objects.create(
        file_name=products_file.name, size=products_file.size,
        file_path = file_path)

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
