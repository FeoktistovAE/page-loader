from page_loader.downloader import download
import requests_mock
import tempfile
import os
from tests import FIXTURE_PATH


def get_content(path, mode='r'):
    with open(path, mode) as output:
        return output.read()


def build_path(file_name):
    return os.path.join(FIXTURE_PATH, file_name)


def test_download_html():
    url = 'https://ru.hexlet.io/courses'
    image_url = get_content(build_path('image_url.txt'))
    html_content = get_content(build_path('fixture1.html'))
    img_content = get_content(build_path('fixture_image.png'), mode='rb')
    expected_content = get_content(build_path('expected1.html'))
    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(url, text=html_content)
            mock.get(image_url, content=img_content)
            expected_html_path = os.path.join(
                tempdir, 'ru-hexlet-io-courses.html'
            )
            image_path = os.path.join(
                tempdir, get_content(build_path('image_path.txt'))
            )
            result_path = download(url, tempdir)
            result_content = get_content(result_path)
            image_content = get_content(image_path, mode='rb')
    assert image_content == img_content
    assert result_path == expected_html_path
    assert result_content == expected_content
