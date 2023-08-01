"""
This module handles http requests to the Confluence API
"""
import dataclasses

import requests
from requests import JSONDecodeError

from pyphluence import logger
from pyphluence.exceptions import BaseURLNotSetException


@dataclasses.dataclass
class ApiResponse:
    """
    ApiResponse packages up the response from the api. This provides an interface for any variations on api callers
    so the server object always knows how to handle the response.
    """
    status_code: int = None
    data: dict = None
    error_msg: str | None = None
    has_errors: bool = False

    def __post_init__(self):
        if self.status_code != 200:
            self.has_errors = True


class ApiCaller:
    """
    This is a wrapper around the requests package. It doesn't extend it but makes it easier to handle
    dependencies in other classes that need to make http calls

    :param base_url: the base url of the confluence server
    :param token: the token to use for authentication
    :param username: the username to use for authentication
    :param cloud: whether the server is a cloud server

    """
    def __init__(self, **kwargs):
        self._headers = {}
        self._cloud = False
        self._username = None
        self._token = None

        if "base_url" not in kwargs:
            raise BaseURLNotSetException("Missing base_url")

        if "token" in kwargs:
            self._token = kwargs["token"]

        if "username" in kwargs:
            self._username = kwargs["username"]

        if "cloud" in kwargs and kwargs["cloud"] is True:
            self._cloud = True

        if "atlassian.net" in kwargs["base_url"]:
            self._cloud = True

        self._base_url = kwargs["base_url"]

        self._session = requests.Session()

        self._init_session_auth()

    def add_header(self, key, value):
        self._headers[key] = value

    def remove_header(self, key):
        del self._headers[key]

    def _init_session_auth(self):

        # cloud server uses basic auth with token instead of password
        if self._cloud and self._username and self._token:
            self._session.auth = (self._username, self._token)

        # data center server uses Personal Access Tokens (PAT)
        if self._token and not self._cloud:
            self.add_header("Authorization", f"Bearer {self._token}")
            self._session.headers.update(self._headers)

    def get(self, api_endpoint: str, params: dict = None) -> ApiResponse:
        """
        Make a GET request to the API

        :param api_endpoint: the endpoint to call
        :param params: the parameters to pass to the endpoint
        :return: the response from the API
        """
        resp = self._session.get("%s%s" % (self._base_url, api_endpoint),
                                 headers=self._headers, params=params)

        return _create_api_response(resp)

    def post(self, api_endpoint: str, data: dict = None) -> ApiResponse:
        """
        Make a POST request to the API

        :param api_endpoint: the endpoint to call
        :param data: the data to pass to the endpoint
        :return: the response from the API
        """
        resp = self._session.post("%s%s" % (self._base_url, api_endpoint),
                                  headers=self._headers, json=data)

        return _create_api_response(resp)

    def put(self, api_endpoint: str, data: dict = None) -> ApiResponse:
        """
        Make a PUT request to the API

        :param api_endpoint: the endpoint to call
        :param data: the data to pass to the endpoint
        :return: the response from the API
        """
        resp = self._session.put("%s%s" % (self._base_url, api_endpoint),
                                 headers=self._headers, json=data)

        return _create_api_response(resp)

    def delete(self, api_endpoint: str) -> ApiResponse:
        """
        Make a DELETE request to the API

        :param api_endpoint: the endpoint to call
        :return: the response from the API
        """
        resp = self._session.delete("%s%s" % (self._base_url, api_endpoint),
                                    headers=self._headers)

        return _create_api_response(resp)


def _create_api_response(resp) -> ApiResponse:
    resp_json = get_json_from_response(resp)
    error = None

    if resp_json is None and not resp.status_code:
        resp.status_code = 400
        resp_json = {}
        error = "Error retrieving data from the server"

    if resp.status_code == 204 or resp.status_code == 202:
        resp_json = {}
        resp.status_code = 200

    if resp.status_code != 200 and 'message' not in resp_json:
        resp_json['message'] = "Unknown Error"

    if resp.status_code == 400:
        error = f"Bad Request: {resp_json['message']}"

    if resp.status_code == 401:
        error = f"Unauthorized: {resp_json['message']}"

    if resp.status_code == 403:
        error = f"Forbidden: {resp_json['message']}"

    if resp.status_code == 404:
        error = f"Not Found: {resp_json['message']}"

    if resp.status_code == 405:
        error = f"Method Not Allowed: {resp_json['message']}"

    if resp.status_code == 409:
        error = f"Conflict: {resp_json['message']}"

    if resp.status_code == 429:
        error = f"Too Many Requests: {resp_json['message']}"

    if resp.status_code == 449:
        error = f"Retry With: {resp_json['message']}"

    if resp.status_code == 500:
        error = f"Internal Server Error: {resp_json['message']}"

    if resp.status_code == 503:
        error = f"Service Unavailable: {resp_json['message']}"

    if resp.status_code == 504:
        error = f"Gateway Timeout: {resp_json['message']}"

    api_resp = ApiResponse(status_code=resp.status_code, data=resp_json, error_msg=error)

    return api_resp


def get_json_from_response(resp):
    """
    Gets the json from the response and returns it
    :param resp:
    :return:
    """

    if resp.status_code == 204:
        return {}

    try:
        json_data = resp.json()
    except JSONDecodeError as e:
        logger.error("Error retrieving data from the server")
        return {}

    return json_data
