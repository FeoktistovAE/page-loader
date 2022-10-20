import requests
import os


def to_file_name(url):
    if url.startswith('https://'):
        domen = url[8:]
    elif url.startswith('http://'):
        domen = url[7:]
    domen = os.path.splitext(domen)[0]
    file_name = domen.replace('.', '-').replace('/', '-')
    return file_name


def download(url, path=os.getcwd(), client=requests):
    response = client.get(url)
    content = response.text
    file_name = to_file_name(url)
    file_path = f'{path}/{file_name}.html'
    with open(file_path, 'w') as f:
        f.write(content)
    return file_path
