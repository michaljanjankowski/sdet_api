import unittest.mock
import requests


class GoogleScrapperMock:
    def __init__(self):
        self.start_mock()

    def start_mock(self):
        requests_Session_patcher = unittest.mock.patch(
            target='requests.Session', autospec=True, side_effect=self
        )
        requests_Session_patcher.start()

    def __call__(self, *args, **kwargs):
        mock = unittest.mock.MagicMock()

        def mocked_get(*args, **kwargs):
            mocked_response = unittest.mock.MagicMock()
            mocked_response.url=kwargs.get("url", "This is mock speaking url not passed")
            mocked_response.status_code = 200
            return mocked_response

        mock.get.side_effect = mocked_get

        return mock


class GoogleScrapper:

    headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    def __init__(self):
        GoogleScrapperMock()

    def make_query(self, query):
        s = requests.Session()
        q = '+'.join(query.split())
        url = f'https://www.google.com/search?q={query}&ie=utf-8&oe=utf-8'
        return s.get(url=url, headers=self.headers_Get)


if __name__ == "__main__":
    googlescrapper = GoogleScrapper()
    result = googlescrapper.make_query("Python")
    assert result.status_code == 200
