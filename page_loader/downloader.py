import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import logging
from progress.bar import IncrementalBar
from page_loader.url import generate_name


HTML_TAGS = (
    ('img', 'src'),
    ('link', 'href'),
    ('script', 'src')
)


def prepare_html_and_resources(url, outdir):
    resources = {}
    response = requests.get(url)
    if response.status_code > 200:
        logging.error(f'Код ответа {response.status_code}')
        raise requests.exceptions.ConnectionError
    html_content = BeautifulSoup(response.text, 'html.parser')
    url_parts = urlparse(url)
    for tag, attribute in HTML_TAGS:
        elements = html_content.find_all(tag)
        for element in elements:
            resource = element.get(attribute)
            if not resource:
                continue
            resource_parts = urlparse(resource)
            resource_extension = os.path.splitext(resource)[1]
            if resource[0] == '/':
                resource_name = generate_name(url_parts[1] + resource, resource_extension)
                resource_path = os.path.join(outdir, resource_name)
                resource_url = urljoin(url, resource)
                resources[resource_url] = resource_path
                element[attribute] = os.path.join(outdir, resource_name)
            elif url_parts[1] == resource_parts[1]:
                resource_without_schema = resource_parts[1] + resource_parts[2]
                resource_name = generate_name(resource_without_schema, resource_extension)
                resource_path = os.path.join(outdir, resource_name)
                resources[resource] = resource_path
                element[attribute] = os.path.join(outdir, resource_name)
    return html_content.prettify(), resources


def download_resources(resources, url, path, outdir):
    bar = IncrementalBar('Downloading:', max=4, suffix="%(percent).1f%%  (eta: %(eta)d)")
    files_dir_path = os.path.join(path, outdir)
    os.mkdir(files_dir_path)
    for resource_url, resource_path in resources.items():
        file_path = os.path.join(path, resource_path)
        response = requests.get(resource_url)
        with open(file_path, 'wb') as content_input:
            content_input.write(response.content)
        bar.next()
    bar.finish()


def download(url, path):
    outdir = generate_name(url, '_files')
    html_content, resources = prepare_html_and_resources(url, outdir)
    download_resources(resources, url, path, outdir)
    html_name = generate_name(url, '.html')
    html_path = os.path.join(path, html_name)
    with open(html_path, 'w') as input:
        input.write(html_content)
    return html_path
