from page_loader.downloader import download
import requests
import pytest
import os
from tests import FIXTURE_PATH


FIXTURE_HTML = 'fixture.html'
FIXTURE_PNG = 'fixture.png'
FIXTURE_CSS = 'fixture.css'
FIXTURE_JS = 'fixture.js'
EXPECTED = 'expected.html'
URL = 'https://ru.hexlet.io/courses'


def get_content(path, mode='r'):
    with open(path, mode) as output:
        return output.read()


def build_path(file_name):
    return os.path.join(FIXTURE_PATH, file_name)


def to_local_path(local_name):
    return 'ru-hexlet-io-courses_files/ru-hexlet-io-' + local_name


def test_download(requests_mock, tmpdir):
    html_content = get_content(build_path(FIXTURE_HTML))
    requests_mock.get(URL, text=html_content)
    expected_content = get_content(build_path(EXPECTED))
    expected_html_path = os.path.join(
        tmpdir, 'ru-hexlet-io-courses.html'
    )

    expected_img_content = get_content(build_path(FIXTURE_PNG), mode='rb')
    expected_css_content = get_content(build_path(FIXTURE_CSS), mode='rb')
    expected_js_content = get_content(build_path(FIXTURE_JS), mode='rb')

    requests_mock.get(
        'https://ru.hexlet.io/assets/application.css', content=expected_css_content
    )
    requests_mock.get(
        'https://ru.hexlet.io/assets/professions/nodejs.png', content=expected_img_content
    )
    requests_mock.get(
        'https://ru.hexlet.io/packs/js/runtime.js', content=expected_js_content
    )
    image_path = os.path.join(
        tmpdir, 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png'
    )
    css_path = os.path.join(
        tmpdir, 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-application.css'
    )
    js_path = os.path.join(
        tmpdir, 'ru-hexlet-io-courses_files/ru-hexlet-io-packs-js-runtime.js'
    )
    html_path = os.path.join(
        tmpdir, 'ru-hexlet-io-courses_files/ru-hexlet-io-courses.html'
    )
    result_path = download(URL, tmpdir)
    print(os.listdir(os.path.join(tmpdir, 'ru-hexlet-io-courses_files')))
    result_content = get_content(result_path)
    image_content = get_content(image_path, mode='rb')
    css_content = get_content(css_path, mode='rb')
    js_content = get_content(js_path, mode='rb')
    expected_html_content = get_content(html_path)
    assert expected_css_content == css_content
    assert expected_js_content == js_content
    assert expected_img_content == image_content
    assert expected_html_path == result_path
    assert result_content == expected_content
    assert expected_html_content == html_content


def test_status_code(requests_mock, tmpdir):
    with pytest.raises(requests.exceptions.ConnectionError):
        requests_mock.get(URL, status_code=404)
        download(URL, tmpdir)


def test_wrong_path_dir(requests_mock):
    with pytest.raises(OSError):
        requests_mock.get(URL)
        download(URL, 'wrong/path/directory')
