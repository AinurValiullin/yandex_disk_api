import uuid
DISK_URL = "https://cloud-api.yandex.net/v1/disk"
RESOURCES_URL = f"{DISK_URL}/resources"
COPY_URL = f"{DISK_URL}/resources/copy"

def get_name(prefix="folder"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"