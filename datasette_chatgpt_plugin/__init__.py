import hashlib
from urllib.parse import urlparse


def name_for_model(url):
    name = urlparse(url).hostname.replace(".", "_").replace("-", "_")
    md5_hash = hashlib.md5(url.encode("utf-8")).hexdigest()[:6]
    output = f"datasette_{name}_{md5_hash}"

    if len(output) > 50:
        excess_length = len(output) - 50
        output = f"datasette_{name[:-excess_length]}_{md5_hash}"

    return output
