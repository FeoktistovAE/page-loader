import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def rename(url, extension):
    if extension == '':
        extension = '.html'
    url_parts = list(urlparse(url))
    url_without_schema = url_parts[1] + url_parts[2]
    url_without_extension = os.path.splitext(url_without_schema)[0]
    name = url_without_extension.replace('.', '-').replace('/', '-')
    return name + extension


def download_html(url, path):
    request = requests.get(url)
    content = request.text
    file_name = rename(url, '.html')
    file_path = os.path.join(path, file_name)
    with open(file_path, 'w') as f:
        f.write(content)
    return file_path


def save_content(
    html_content, files_dir_path, files_dir_name, url, content_type, attribute
):
    url_parts = urlparse(url)
    all_sources = html_content.find_all(content_type)
    for i in all_sources:
        try:
            source = i[attribute]
            source_parts = urlparse(source)
            if source_parts[1] == '':
                source_extension = os.path.splitext(source)[1]
                source_name = rename(url_parts[1] + source, source_extension)
                source_path = os.path.join(files_dir_path, source_name)
                source_url = f'{url_parts[0]}://{url_parts[1]}{source}'
                request = requests.get(source_url)
                with open(source_path, 'wb') as content_input:
                    content_input.write(request.content)
                i[attribute] = os.path.join(files_dir_name, source_name)
            elif source_parts[1] == url_parts[1]:
                source_extension = os.path.splitext(source)[1]
                source_without_schema = source_parts[1] + source_parts[2]
                source_name = rename(source_without_schema, source_extension)
                source_path = os.path.join(files_dir_path, source_name)
                request = requests.get(source)
                with open(source_path, 'wb') as content_input:
                    content_input.write(request.content)
                i[attribute] = os.path.join(files_dir_name, source_name)
        except KeyError:
            print('KeyError')
        except requests.exceptions.InvalidURL:
            print('invalidURL')


def download(url, path):
    file_path = download_html(url, path)
    with open(file_path) as html_doc:
        html_content = BeautifulSoup(html_doc, 'html.parser')
    files_dir_name = rename(url, '_files')
    files_dir_path = os.path.join(path, files_dir_name)
    os.mkdir(files_dir_path)
    save_content(html_content, files_dir_path, files_dir_name, url, 'img', 'src')
    save_content(html_content, files_dir_path, files_dir_name, url, 'link', 'href')
    save_content(html_content, files_dir_path, files_dir_name, url, 'script', 'src')
    with open(file_path, 'w') as input:
        input.write(html_content.prettify())
    return file_path
