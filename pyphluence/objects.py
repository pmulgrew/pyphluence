"""
This module contains the objects used to interact with the Confluence API
"""
from __future__ import annotations

from pyphluence.exceptions import PyfluenceIDNotSetException
from pyphluence.http import ApiCaller
from . import logger


class ApiModel:
    def __init__(self, api_caller: ApiCaller = None):
        self._api_caller = api_caller
        self._data = {}
        self._expands = []
        self._api_endpoints = {"get": "", "create": "", "update": "", "delete": ""}
        self._primary_identifier = "id"
        self._last_response = None

    @property
    def id(self):
        return self._data.get('id', None)

    @id.setter
    def id(self, obj_id):
        self._data['id'] = obj_id

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
            return True  # Assume error if no response

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

        self._last_response = self._api_caller.get(self._get_endpoint("get"),
                                                   params={"expand": ",".join(self._expands)})
        self._data = self._last_response.data

    def save(self):
        update = self._is_update()

        if not update:
            self._last_response = self._api_caller.post(self._get_endpoint("create"), data=self._data)
            logger.debug("Creating page")

        if update:
            self._last_response = self._api_caller.put(self._get_endpoint("update"), data=self._data)
            logger.debug("Updating page")

        self._data = self._last_response.data
        self._update_endpoints()

    def _is_update(self):
        if getattr(self, "id"):
            return True

        return False

    def delete(self):
        if not getattr(self, self._primary_identifier):
            raise PyfluenceIDNotSetException(f"Primary identifier ({self._primary_identifier}) not set. Unable to "
                                             f"retrieve data.")

        self._last_response = self._api_caller.delete(self._get_endpoint("delete"))

        if self.status_code == 200:
            self._data = {}


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

        self._data['type'] = "page"

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

    @status.setter
    def status(self, status):
        self._data['status'] = status

    @property
    def version(self):
        if 'version' not in self._data:
            return None

        return self._data['version']['number']

    @version.setter
    def version(self, version):
        if 'version' not in self._data:
            self._data['version'] = {}

        self._data['version']['number'] = version

    @property
    def space_key(self):
        if 'space' not in self._data:
            return None

        return self._data['space']['key']

    @space_key.setter
    def space_key(self, space_key):
        if 'space' not in self._data:
            self._data['space'] = {}

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
        if 'body' not in self._data:
            self._data['body'] = {}

        if 'storage' not in self._data['body']:
            self._data['body']['storage'] = {}

        self._data['body']['storage']['value'] = body
        self._data['body']['storage']['representation'] = "storage"

    @property
    def parent(self) -> Page | None:
        """
        Returns the parent page object if it exists.

        :return:
        """
        if 'ancestors' not in self._data:
            self.add_expand("ancestors")
            self.get()

        if len(self._data['ancestors']) == 0:
            return None

        parent = Page(self._api_caller)
        parent.id = self._data['ancestors'][0]['id']
        parent.get()

        return parent

    @parent.setter
    def parent(self, parent_page: Page | int = None):
        """
        Sets the parent page of the page. Can pass in a Page object or an int of the page id.

        :param parent_page:
        :return:
        """
        parent_id = None

        if isinstance(parent_page, str):
            parent_id = int(parent_page)

        if isinstance(parent_page, Page):
            parent_id = parent_page.id

        if isinstance(parent_page, int):
            parent_id = parent_page

        if 'ancestors' not in self._data:
            self._data['ancestors'] = []

        self._data['ancestors'].insert(0, {'id': parent_id})

    def save(self):
        """
        Saves the page to Confluence. If the page does not exist, it will be created.

        :return:
        """
        self.surpress_notifications()

        if self._is_update():
            self.version += 1

        super().save()

    def surpress_notifications(self):
        """
       stops emails being sent when the page is saved.

        :return:
        """
        self._data['version']['minorEdit'] = True



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
        self._scan_results = None
        self._primary_identifier = "key"
        self._api_endpoints = {
            "get": "/rest/api/space/{primary}",
            "create": "/rest/api/space",
            "update": "/rest/api/space/{primary}",
            "delete": "/rest/api/space/{primary}",
            "scan": "/rest/api/content/scan"
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

    @property
    def type(self):
        if 'type' not in self._data:
            return None

        return self._data['type']

    @type.setter
    def type(self, space_type):
        self._data['type'] = space_type

    @property
    def status(self):
        if 'status' not in self._data:
            return None

        return self._data['status']

    @status.setter
    def status(self, space_status):
        self._data['status'] = space_status

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

        parent_id = parent_id or self.homepage_id

        page = Page(self._api_caller)
        page.space_key = self.key
        page.title = title
        page.body = body
        page.parent_id = parent_id

        return page

    def scan(self, status="any", expand=None, cursor=None, limit=25):
        """
        uses the confluence scan endpoint to get pages based on status

        only available on server/data center
        :return:
        """
        logger.debug(f"Scanning space {self.key} for pages with status {status}")

        if not cursor:
            self._scan_results = []

        params = {
            "spaceKey": self.key,
            "status": status,
        }

        if expand:
            params['expand'] = expand

        if cursor:
            params['cursor'] = cursor

        if limit and limit != 25:
            params['limit'] = limit

        response = self._api_caller.get(self._get_endpoint("scan"), params=params)

        if response.has_errors:
            return None

        self._last_response = response

        for result in response.data['results']:
            self._scan_results.append(result)

        if "nextCursor" in response.data:
            self.scan(status=status, cursor=response.data['nextCursor'], limit=limit, expand=expand)

        return self._scan_results

    def restore_page(self, page_id, version=None, parent_id=None):
        """
        Restores a page from the trash.

        :param parent_id:
        :param page_id:
        :param version:
        :return:
        """
        restore = Page(self._api_caller)
        restore.id = page_id
        restore.version = version
        restore.status = "current"

        restore.save()

        if parent_id:
            restore.get()
            restore.parent = parent_id
            restore.save()
