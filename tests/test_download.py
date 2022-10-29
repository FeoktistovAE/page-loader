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


def test_download():
    url = 'https://ru.hexlet.io/courses'
    html_content = get_content(build_path('fixture1.html'))
    expected_img_content = get_content(build_path('fixture_image.png'), mode='rb')
    expected_css_content = get_content(build_path('fixture.css'), mode='rb')
    expected_js_content = get_content(build_path('fixture.js'), mode='rb')
    expected_content = get_content(build_path('expected1.html'))
    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(url, text=html_content)
            mock.get(
                'https://ru.hexlet.io/assets/application.css', content=expected_css_content
            )
            mock.get(
                'https://ru.hexlet.io/assets/professions/nodejs.png', content=expected_img_content
            )
            mock.get(
                'https://ru.hexlet.io/packs/js/runtime.js', content=expected_js_content
            )

            expected_html_path = os.path.join(
                tempdir, 'ru-hexlet-io-courses.html'
            )
            image_path = os.path.join(
                tempdir, 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-professions-nodejs.png'
            )
            css_path = os.path.join(
                tempdir, 'ru-hexlet-io-courses_files/ru-hexlet-io-assets-application.css'
            )
            js_path = os.path.join(
                tempdir, 'ru-hexlet-io-courses_files/ru-hexlet-io-packs-js-runtime.js'
            )
            html_path = os.path.join(
                tempdir, 'ru-hexlet-io-courses_files/ru-hexlet-io-courses.html'
            )
            result_path = download(url, tempdir)
            print(os.listdir(os.path.join(tempdir, 'ru-hexlet-io-courses_files')))
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
