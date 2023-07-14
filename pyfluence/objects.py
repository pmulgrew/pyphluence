"""
This module contains the objects used to interact with the Confluence API
"""
from pyfluence.exceptions import PyfluenceIDNotSetException
from pyfluence.http import ApiCaller
from __future__ import annotations


class ApiModel:
    def __init__(self, api_caller: ApiCaller = None):
        self._api_caller = api_caller
        self._data = {}
        self._expands = []
        self._api_endpoints = {"get": "", "create": "", "update": "", "delete": ""}
        self._primary_identifier = "id"
        self._last_response = None

    @property
    def status_code(self) -> int | None:
        if not self._last_response:
            return None

        return self._last_response.status_code

    @property
    def error(self) -> str | None:
        if not self._last_response:
            return "Data no set. Try calling get() first."

        return self._last_response.error_msg

    @property
    def has_errors(self) -> bool:
        if not self._last_response:
            return True # Assume error if no response

        return self._last_response.has_errors

    @property
    def url(self):
        if '_links' not in self._data:
            return None

        return f"{self._data['_links']['base']}{self._data['_links']['webui']}"

    def add_expand(self, expand):
        """
        Expands are used to get more information about the confluence object

        Available Expands
        -----------------
        ancestors
        body.storage
        body.view
        children
        history
        space
        version
        metadata

        :param expand:
        :return:
        """
        if expand not in self._expands:
            self._expands.append(expand)

    def remove_expand(self, expand):
        if expand in self._expands:
            self._expands.remove(expand)

    def _add_endpoint(self, key, value):
        self._api_endpoints[key] = value

    def _get_endpoint(self, endpoint):
        return self._api_endpoints[endpoint]

    def _update_endpoints(self):
        if getattr(self, self._primary_identifier):
            for key, endpoint in self._api_endpoints.items():
                self._api_endpoints[key] = endpoint.format(primary=getattr(self, self._primary_identifier))

    def get(self):

        if not getattr(self, self._primary_identifier):
            raise PyfluenceIDNotSetException(f"Primary identifier ({self._primary_identifier}) not set. Unable to "
                                             f"retrieve data.")

        self._last_response = self._api_caller.get(self._get_endpoint("get"), params={"expand": ",".join(self._expands)})
        self._data = self._last_response.data


class Page(ApiModel):

    def __init__(self, api_caller: ApiCaller = None):
        super().__init__(api_caller)
        self._primary_identifier = "id"
        self._api_endpoints = {
            "get": "/rest/api/content/{primary}",
            "create": "/rest/api/content",
            "update": "/rest/api/content/{primary}",
            "delete": "/rest/api/content/{primary}",
            "labels": "/rest/api/content/{primary}/label/",
        }

        # this is all the available representations for the body of a page
        self._body_representations = [
            "storage",
            "view",
            "export_view",
            "anonymous_export_view"
        ]

        # all pages should have these expands by default
        self.add_expand("body.storage")
        self.add_expand("space")
        self.add_expand("version")
        self.add_expand("ancestors")
        self.add_expand("metadata.labels")

    @property
    def id(self):
        if 'id' not in self._data:
            return None

        return int(self._data['id'])

    @id.setter
    def id(self, page_id):
        self._data['id'] = page_id
        # when the id is set, we need to update the endpoints
        self._update_endpoints()

    @property
    def title(self):
        if 'title' not in self._data:
            return None

        return self._data['title']

    @title.setter
    def title(self, title):
        self._data['title'] = title

    @property
    def type(self):
        if 'type' not in self._data:
            return None

        return self._data['type']

    @property
    def status(self):
        if 'status' not in self._data:
            return None

        return self._data['status']

    @property
    def version(self):
        if 'version' not in self._data:
            return None

        return self._data['version']['number']

    @version.setter
    def version(self, version):
        self._data['version']['number'] = version

    @property
    def space_key(self):
        if 'space' not in self._data:
            return None

        return self._data['space']['key']

    @space_key.setter
    def space_key(self, space_key):
        self._data['space']['key'] = space_key

    @property
    def body(self):
        """
        Returns the body of the page. Storage is return using .body for other modes use .get_body_representation(mode)

        :return:
        """
        if 'body' not in self._data:
            return None

        if 'storage' not in self._data['body']:
            self.add_expand("body.storage")
            self.get()

        if 'value' not in self._data['body']['storage']:
            return None

        return self._data['body']['storage']['value']

    @body.setter
    def body(self, body):
        """
        Sets the body of the page in storage representation mode.
        :param body:
        :return:
        """
        self._data['body']['storage']['value'] = body

    @property
    def parent(self) -> Page | None:
        """
        Returns the parent page object if it exists.

        :return:
        """
        if 'ancestors' not in self._data:
            self.add_expand("ancestors")
            self.get()

        if 'results' not in self._data['ancestors']:
            return None

        if len(self._data['ancestors']) == 0:
            return None

        parent = Page(self._api_caller)
        parent.id = self._data['ancestors']['results'][0]['id']
        parent.get()

        return parent

    @parent.setter
    def parent(self, parent_page: Page | int = None):
        """
        Sets the parent page of the page.

        :param parent_page:
        :return:
        """
        if isinstance(parent_page, Page):
            id = parent_page.id

        elif isinstance(parent_page, int):
            id = parent_page

        else:
            id = None

        self._data['ancestors'][0]['id'] = id

    def get_body_representation(self, mode):
        """
        Returns the body representation for the given mode. If the mode is not valid, returns None.

        :param mode:
        :return:
        """
        if mode not in self._body_representations:
            return None

        if f"body.{mode}" not in self._expands:
            self.add_expand(f"body.{mode}")
            self.get()

        if mode not in self._data['body']:
            return None

        if 'value' not in self._data['body'][mode]:
            return None

        return self._data['body'][mode]['value']

    def labels(self):
        """
        Returns the labels for the page.

        :return:
        """
        if 'metadata' not in self._data:
            self.add_expand("metadata.labels")
            self.get()

        if 'labels' not in self._data['metadata']:
            return None

        labels = [label['label'] for label in self._data['metadata']['labels']['results']]

        return labels

    def add_label(self, label):
        """
        Adds a label to the page.

        :param label:
        :return:
        """

        label = {
            "prefix": "global",
            "name": label
        }

        self._api_caller.post(self._get_endpoint("labels"), data=label)

    def remove_label(self, label):
        """
        Removes a label from the page.

        :param label:
        :return:
        """

        self._api_caller.delete(f"{self._get_endpoint('labels')}{label}")

    def remove_all_labels(self):
        """
        Removes all labels from the page.

        :return:
        """

        for label in self.labels():
            self.remove_label(label)


class Space(ApiModel):
    def __init__(self, api_caller: ApiCaller):
        super().__init__(api_caller)
        self._primary_identifier = "key"
        self._api_endpoints = {
            "get": "/rest/api/space/{primary}",
            "create": "/rest/api/space",
            "update": "/rest/api/space/{primary}",
            "delete": "/rest/api/space/{primary}",
        }

        self.add_expand("description.plain")
        self.add_expand("homepage")

    @property
    def key(self):
        if 'key' not in self._data:
            return None

        return self._data['key']

    @key.setter
    def key(self, space_key):
        self._data['key'] = space_key
        self._update_endpoints()
        self.get()

    @property
    def name(self):
        if 'name' not in self._data:
            return None

        return self._data['name']

    @name.setter
    def name(self, name):
        self._data['name'] = name

    @property
    def description(self):
        if 'description' not in self._data:
            return None

        return self._data['description']['plain']['value']

    @description.setter
    def description(self, description):
        self._data['description']['plain']['value'] = description

    @property
    def homepage_id(self):
        if 'homepage' not in self._data:
            return None

        return self._data['homepage']['id']

    @property
    def id(self):
        if 'id' not in self._data:
            return None

        return self._data['id']

    @property
    def homepage(self) -> Page | None:
        if 'homepage' not in self._data:
            return None

        homepage = Page(self._api_caller)
        homepage.id = self.homepage_id
        homepage.get()

        return homepage

    def get_page(self, page_id):
        if self.has_errors:
            raise ValueError(self.error)

        page = Page(self._api_caller)
        page.id = page_id
        page.get()

        # if the page exists but is not in this space, return a 404
        if page.space_key != self.key:
            page._last_response.error_msg = f"Page {page_id} is not in space {self.key}"
            page._last_response.status_code = 404
            page._last_response.has_errors = True

        return page

    def new_page(self, title: str = None, body: str = None, parent_id=None):
        if self.has_errors:
            raise ValueError(self.error)

        page = Page(self._api_caller)
        page.space_key = self.key
        page.title = title
        page.body = body
        page.parent_id = parent_id

        return page
