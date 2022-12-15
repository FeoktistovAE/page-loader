import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import logging
from progress.bar import IncrementalBar
from page_loader.known_error import KnownError


HTML_TAGS = (
    ('img', 'src'),
    ('link', 'href'),
    ('script', 'src')
)


def rename(url, extension):
    if extension == '':
        extension = '.html'
    url_parts = list(urlparse(url))
    url_without_schema = url_parts[1] + url_parts[2]
    url_without_extension = os.path.splitext(url_without_schema)[0]
    name = url_without_extension.replace('.', '-').replace('/', '-')
    return name + extension


def get_html_and_resources(url, outdir):
    resources = {}
    try:
        request = requests.get(url)
        if request.status_code > 200:
            logging.error(f'Код ответа {request.status_code}')
            raise KnownError
        html_content = BeautifulSoup(request.text, 'html.parser')
        url_parts = urlparse(url)
        for tag, attribute in HTML_TAGS:
            elements = html_content.find_all(tag)
            for element in elements:
                resource = element[attribute]
                resource_parts = urlparse(resource)
                resource_extension = os.path.splitext(resource)[1]
                if resource[0] == '/':
                    resource_name = rename(url_parts[1] + resource, resource_extension)
                    resource_path = os.path.join(outdir, resource_name)
                    resource_url = urljoin(url, resource)
                    resources[resource_url] = resource_path
                    element[attribute] = os.path.join(outdir, resource_name)
                elif url_parts[1] == resource_parts[1]:
                    resource_without_schema = resource_parts[1] + resource_parts[2]
                    resource_name = rename(resource_without_schema, resource_extension)
                    resource_path = os.path.join(outdir, resource_name)
                    resources[resource] = resource_path
                    element[attribute] = os.path.join(outdir, resource_name)
    except KeyError as e:
        logging.debug(e)
    except requests.exceptions.InvalidURL as e:
        logging.debug(e)
    except requests.exceptions.ConnectionError as e:
        logging.debug(e)
        logging.error('Не удалось загрузить страницу')
        raise KnownError from e
    except requests.exceptions.MissingSchema as e:
        logging.debug(e)
        logging.error(f'Отсутсвует схема в набранном URL, возможно вы имели в виду http://{url}?')
        raise KnownError from e
    return html_content.prettify(), resources


def download_resources(resources, url, path):
    bar = IncrementalBar('Downloading:', max=4, suffix="%(percent).1f%%  (eta: %(eta)d)")
    files_dir_name = rename(url, '_files')
    files_dir_path = os.path.join(path, files_dir_name)
    try:
        os.mkdir(files_dir_path)
    except OSError as e:
        logging.debug(e)
        logging.error(f'Директории "{path}" не существует, либо к ней ограничен доступ')
        raise KnownError from e
    for resource_url, resource_path in resources.items():
        file_path = os.path.join(path, resource_path)
        try:
            request = requests.get(resource_url)
            with open(file_path, 'wb') as content_input:
                content_input.write(request.content)
        except KeyError as e:
            logging.debug(e)
        except requests.exceptions.InvalidURL as e:
            logging.debug(e)
        bar.next()
    bar.finish()


def download(url, path):
    outdir = rename(url, '_files')
    html_content, resources = get_html_and_resources(url, outdir)
    download_resources(resources, url, path)
    html_name = rename(url, '.html')
    html_path = os.path.join(path, html_name)
    with open(html_path, 'w') as input:
        input.write(html_content)
    return html_path
