from page_loader.downloader import download
import requests_mock
import tempfile


def test_download():
        url = 'https://ru.hexlet.io/courses'
        with tempfile.TemporaryDirectory() as tempdir:
            with requests_mock.Mocker() as mock:
                mock.get(url, text='data')
                excepted = f'{tempdir}/ru-hexlet-io-courses.html'
                file_path = download(url, path=tempdir)
                with open(file_path) as output:
                    expected_content = output.read()
                    assert expected_content== 'data'
                assert file_path == excepted


