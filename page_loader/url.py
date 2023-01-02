from urllib.parse import urlparse
import os


def to_file(url, extension):
    if extension == '':
        extension = '.html'
    parsed_url = urlparse(url)
    url_without_schema = parsed_url.netloc + parsed_url.path
    url_without_extension = os.path.splitext(url_without_schema)[0]
    name = url_without_extension.replace('.', '-').replace('/', '-')
    return name + extension
