import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def rename(url, extension):
    url_parts = list(urlparse(url))
    url_without_schema = url_parts[1] + url_parts[2]
    url_without_extension = os.path.splitext(url_without_schema)[0]
    name = url_without_extension.replace('.', '-').replace('/', '-')
    return name + extension


def save_image(file_path, url, path):
    with open(file_path) as html_doc:
        soup = BeautifulSoup(html_doc, 'html.parser')
    image_dir_name = rename(url, '_files')
    image_dir_path = os.path.join(path, image_dir_name)
    os.mkdir(image_dir_path)
    images = soup.find_all('img')
    for i in images:
        image_url = i['src']
        image_extension = os.path.splitext(image_url)[1]
        image_name = rename(image_url, image_extension)
        image_path = os.path.join(image_dir_path, image_name)
        response = requests.get(image_url)
        with open(image_path, 'wb') as image_content:
            image_content.write(response.content)
        i['src'] = os.path.join(image_dir_name, image_name)
    with open(file_path, 'w') as input:
        input.write(soup.prettify())


def download_html(url, path):
    response = requests.get(url)
    content = response.text
    file_name = rename(url, '.html')
    file_path = os.path.join(path, file_name)
    with open(file_path, 'w') as f:
        f.write(content)
    return file_path


def download(url, path):
    file_path = download_html(url, path)
    save_image(file_path, url, path)
    return file_path
