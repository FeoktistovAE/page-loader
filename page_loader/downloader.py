import requests
import os
import logging
from progress.bar import IncrementalBar
from page_loader.url import to_file
from page_loader.html import prepare_html_and_resources


def download_resource(path, resource_path, resource_url):
    file_path = os.path.join(path, resource_path)
    response = requests.get(resource_url)
    with open(file_path, 'wb') as content:
        content.write(response.content)


def download_resources(resources, path, outdir):
    if not resources:
        logging.debug('Нет ресурсов для скачивания')
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
