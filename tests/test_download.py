from page_loader.downloader import download
import pytest
import os
from tests import FIXTURE_PATH


URL = 'https://ru.hexlet.io/courses'
FILE_NAME = 'ru-hexlet-io-courses.html'

MEDIA_ASSETS = (
    (
        URL,
        'expected.html',
        FILE_NAME,
    ),
    (
        'https://ru.hexlet.io/assets/application.css',
        'fixture.css',
        'ru-hexlet-io-courses_files/ru-hexlet-io-assets-application.css',
    ),
    (
        'https://ru.hexlet.io/assets/professions/nodejs.png',
        'fixture.png',
        'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png',
    ),
    (
        'https://ru.hexlet.io/packs/js/runtime.js',
        'fixture.js',
        'ru-hexlet-io-courses_files/ru-hexlet-io-packs-js-runtime.js',
    ),
    (
        'https://ru.hexlet.io/courses',
        'fixture.html',
        'ru-hexlet-io-courses_files/ru-hexlet-io-courses.html',
    ),
)


def get_content(path):
    with open(path, 'rb') as output:
        return output.read()


def build_path(file_name):
    return os.path.join(FIXTURE_PATH, file_name)


def test_download(requests_mock, tmpdir):
    for url, file, _ in MEDIA_ASSETS:
        file_content = get_content(build_path(file))
        requests_mock.get(url, content=file_content)

    result_path = download(URL, tmpdir)
    expected_path = os.path.join(tmpdir, FILE_NAME)
    assert result_path == expected_path

    for _, file, path in MEDIA_ASSETS:
        expected_content = get_content(build_path(file))
        file_path = os.path.join(tmpdir, path)
        result_content = get_content(file_path)
        assert expected_content == result_content


def test_status_code(requests_mock, tmpdir):
    with pytest.raises(Exception):
        requests_mock.get(URL, status_code=404)
        download(URL, tmpdir)


def test_wrong_path_dir(requests_mock):
    with pytest.raises(OSError):
        requests_mock.get(URL)
        download(URL, 'wrong/path/directory')
