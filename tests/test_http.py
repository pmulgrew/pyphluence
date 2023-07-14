import pyfluence.http as network
import unittest
from unittest import mock


class MockResponse:
    def __init__(self, status_code=200, json_data=None, raise_for_status=None):
        self.status_code = status_code
        self.json_data = json_data
        self.raise_for_status = raise_for_status

    def json(self):
        return self.json_data


def mock_get_200(*args, **kwargs):
    return MockResponse(status_code=200, json_data={"test": "test"})


def mock_get_201(*args, **kwargs):
    return MockResponse(status_code=201, json_data={"test": "test"})


def mock_get_204(*args, **kwargs):
    return MockResponse(status_code=204, json_data={"test": "test"})


def mock_get_400(*args, **kwargs):
    return MockResponse(status_code=400, json_data={"test": "test"})


def mock_get_401(*args, **kwargs):
    return MockResponse(status_code=401, json_data={"test": "test"})


def mock_get_403(*args, **kwargs):
    return MockResponse(status_code=403, json_data={"test": "test"})


def mock_get_404(*args, **kwargs):
    return MockResponse(status_code=404, json_data={"test": "test"})


def mock_get_405(*args, **kwargs):
    return MockResponse(status_code=405, json_data={"test": "test"})


def mock_get_409(*args, **kwargs):
    return MockResponse(status_code=409, json_data={"test": "test"})


def mock_get_429(*args, **kwargs):
    return MockResponse(status_code=429, json_data={"test": "test"})


def mock_get_449(*args, **kwargs):
    return MockResponse(status_code=449, json_data={"test": "test"})


def mock_get_500(*args, **kwargs):
    return MockResponse(status_code=500, json_data={"test": "test"})


def mock_get_503(*args, **kwargs):
    return MockResponse(status_code=503, json_data={"test": "test"})


def mock_get_504(*args, **kwargs):
    return MockResponse(status_code=504, json_data={"test": "test"})


class TestApiCaller(unittest.TestCase):

    def test_no_base_url(self):
        with self.assertRaises(network.BaseURLNotSetException):
            network.ApiCaller()

    def test_base_url(self):
        api = network.ApiCaller(base_url="http://localhost:8080")
        self.assertEqual(api._base_url, "http://localhost:8080")

    def test_cloud(self):
        api = network.ApiCaller(base_url="https://example.atlassian.net")
        self.assertTrue(api._cloud)

    def test_not_cloud(self):
        api = network.ApiCaller(base_url="http://localhost:8080")
        self.assertFalse(api._cloud)

    def test_cloud_override(self):
        api = network.ApiCaller(base_url="http://localhost:8080", cloud=True)
        self.assertTrue(api._cloud)

    def test_not_cloud_atlassian(self):
        api = network.ApiCaller(base_url="https://example.atlassian.net", cloud=False)
        self.assertTrue(api._cloud)

    def test_add_header(self):
        api = network.ApiCaller(base_url="http://localhost:8080")
        api.add_header("test", "value")
        self.assertEqual(api._headers["test"], "value")

    def test_remove_header(self):
        api = network.ApiCaller(base_url="http://localhost:8080")
        api.add_header("test", "value")
        api.remove_header("test")
        self.assertFalse("test" in api._headers)

    def test_init_session_auth_cloud(self):
        api = network.ApiCaller(base_url="https://example.atlassian.net", username="user", token="token")
        self.assertEqual(api._session.auth, ("user", "token"))

    @mock.patch('requests.Session.get', side_effect=mock_get_404)
    def test_404(self, mock_get_404):
        api = network.ApiCaller(base_url="http://localhost:8080")
        resp = api.get("/rest/api/content/999999")
        self.assertEqual(resp.status_code, 404)

    @mock.patch('requests.Session.get', side_effect=mock_get_200)
    def test_200(self, mock_get_200):
        api = network.ApiCaller(base_url="http://localhost:8080")
        resp = api.get("/rest/api/content/1")
        self.assertEqual(resp.status_code, 200)

    @mock.patch('requests.Session.get', side_effect=mock_get_500)
    def test_500(self, mock_get_500):
        api = network.ApiCaller(base_url="http://localhost:8080")
        resp = api.get("/rest/api/content/1")
        self.assertEqual(resp.status_code, 500)

    @mock.patch('requests.Session.get', side_effect=mock_get_401)
    def test_401(self, mock_get_401):
        api = network.ApiCaller(base_url="http://localhost:8080")
        resp = api.get("/rest/api/content/1")
        self.assertEqual(resp.status_code, 401)

    @mock.patch('requests.Session.get', side_effect=mock_get_403)
    def test_403(self, mock_get_403):
        api = network.ApiCaller(base_url="http://localhost:8080")
        resp = api.get("/rest/api/content/1")
        self.assertEqual(resp.status_code, 403)

    @mock.patch('requests.Session.get', side_effect=mock_get_405)
    def test_405(self, mock_get_405):
        api = network.ApiCaller(base_url="http://localhost:8080")
        resp = api.get("/rest/api/content/1")
        self.assertEqual(resp.status_code, 405)

    @mock.patch('requests.Session.get', side_effect=mock_get_409)
    def test_409(self, mock_get_409):
        api = network.ApiCaller(base_url="http://localhost:8080")
        resp = api.get("/rest/api/content/1")
        self.assertEqual(resp.status_code, 409)

    @mock.patch('requests.Session.get', side_effect=mock_get_429)
    def test_429(self, mock_get_429):
        api = network.ApiCaller(base_url="http://localhost:8080")
        resp = api.get("/rest/api/content/1")
        self.assertEqual(resp.status_code, 429)

    @mock.patch('requests.Session.get', side_effect=mock_get_449)
    def test_449(self, mock_get_449):
        api = network.ApiCaller(base_url="http://localhost:8080")
        resp = api.get("/rest/api/content/1")
        self.assertEqual(resp.status_code, 449)

    @mock.patch('requests.Session.get', side_effect=mock_get_503)
    def test_503(self, mock_get_503):
        api = network.ApiCaller(base_url="http://localhost:8080")
        resp = api.get("/rest/api/content/1")
        self.assertEqual(resp.status_code, 503)

    @mock.patch('requests.Session.get', side_effect=mock_get_504)
    def test_504(self, mock_get_504):
        api = network.ApiCaller(base_url="http://localhost:8080")
        resp = api.get("/rest/api/content/1")
        self.assertEqual(resp.status_code, 504)

    @mock.patch('requests.Session.get', side_effect=mock_get_200)
    def test_get(self, mock_get_200):
        api = network.ApiCaller(base_url="http://localhost:8080")
        resp = api.get("/rest/api/content/1")
        self.assertEqual(resp.data['test'], 'test')


if __name__ == '__main__':
    unittest.main()
