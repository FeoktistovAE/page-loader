import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import logging
from progress.bar import IncrementalBar
from page_loader.url import to_file


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
    parsed_url = urlparse(url)
    for tag, attribute in HTML_TAGS:
        elements = html_content.find_all(tag)
        for element in elements:
            resource = element.get(attribute)
            if not resource:
                continue
            parsed_resource = urlparse(resource)
            resource_extension = os.path.splitext(resource)[1]
            if urlparse(resource).netloc == '':
                resource_name = to_file(parsed_url.netloc + resource, resource_extension)
                resource_path = os.path.join(outdir, resource_name)
                resource_url = urljoin(url, resource)
                resources[resource_url] = resource_path
                element[attribute] = os.path.join(outdir, resource_name)
            elif parsed_url.netloc == parsed_resource.netloc:
                resource_without_schema = parsed_resource.netloc + parsed_resource.path
                resource_name = to_file(resource_without_schema, resource_extension)
                resource_path = os.path.join(outdir, resource_name)
                resources[resource] = resource_path
                element[attribute] = os.path.join(outdir, resource_name)
    return html_content.prettify(), resources


def download_resource(path, resource_path, resource_url):
    file_path = os.path.join(path, resource_path)
    response = requests.get(resource_url)
    logging.debug(response.raise_for_status())
    with open(file_path, 'wb') as content_input:
        content_input.write(response.content)


def download_resources(resources, path, outdir):
    if not resources:
        logging.debug(f'Нет ресурсов для скачивания')
        return
    bar = IncrementalBar('Downloading:', max=4, suffix="%(percent).1f%%  (eta: %(eta)d)")
    files_dir_path = os.path.join(path, outdir)
    os.mkdir(files_dir_path)
    for resource_url, resource_path in resources.items():
        download_resource(path, resource_path, resource_url)
        bar.next()
    bar.finish()


def download(url, path):
    outdir = to_file(url, '_files')
    html_content, resources = prepare_html_and_resources(url, outdir)
    download_resources(resources, path, outdir)
    html_result_path = os.path.join(path, to_file(url, '.html'))
    with open(html_result_path, 'w') as input:
        input.write(html_content)
    return html_result_path
