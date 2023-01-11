import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os
from page_loader.url import to_file


HTML_TAGS = (
    ('img', 'src'),
    ('link', 'href'),
    ('script', 'src')
)


def prepare_html_and_resources(url, outdir):
    resources = {}
    response = requests.get(url)
    response.raise_for_status()
    html_content = BeautifulSoup(response.text, 'html.parser')
    parsed_url = urlparse(url)
    for tag, attribute in HTML_TAGS:
        elements = html_content.find_all(tag)
        for element in elements:
            resource = element.get(attribute)
            if not resource:
                continue
            parsed_resource = urlparse(resource)
            resource_extension = os.path.splitext(resource)[1]
            if urlparse(resource).netloc == '' or parsed_url.netloc == parsed_resource.netloc:
                resource_name = to_file(parsed_url.netloc + parsed_resource.path, resource_extension)
                resource_path = os.path.join(outdir, resource_name)
                resource_url = urljoin(url, resource)
                resources[resource_url] = resource_path
                element[attribute] = os.path.join(outdir, resource_name)
    return html_content.prettify(), resources
