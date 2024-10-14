from PIL import Image
from io import BytesIO
from azure.storage.blob import BlobServiceClient
import os

def resize_image(image_stream, max_size):
    img = Image.open(image_stream)

    # Resize dimensions if the image is too large
    max_dimension = 1024  # Example max dimension, adjust as needed
    if max(img.size) > max_dimension:
        img.thumbnail((max_dimension, max_dimension), Image.LANCZOS)

    # Resize logic to ensure image is within 1MB
    output_stream = BytesIO()
    quality = 85  # Start with 85% quality for JPG
    while True:
        output_stream.seek(0)
        img.save(output_stream, format='JPEG', quality=quality)
        size = output_stream.tell()

        if size <= max_size or quality <= 10:
            break

        quality -= 5  # Reduce quality if still too large

    output_stream.seek(0)
    return output_stream


def upload_to_blob(image_stream, filename):
    # Azure Blob Service
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = os.getenv('AZURE_CONTAINER_NAME')

    # Create the BlobClient
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

    # Upload image to blob
    blob_client.upload_blob(image_stream, blob_type="BlockBlob", overwrite=True)

    # Get URL of the uploaded image
    blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{filename}"
    return blob_url

