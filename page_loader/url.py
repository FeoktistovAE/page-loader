from urllib.parse import urlparse
import os


def generate_name(url, extension):
    if extension == '':
        extension = '.html'
    url_parts = list(urlparse(url))
    url_without_schema = url_parts[1] + url_parts[2]
    url_without_extension = os.path.splitext(url_without_schema)[0]
    name = url_without_extension.replace('.', '-').replace('/', '-')
    return name + extension
