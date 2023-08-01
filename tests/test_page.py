import unittest
from unittest import mock

from pyphluence.exceptions import PyfluenceIDNotSetException
from pyphluence.http import ApiCaller, ApiResponse
from pyphluence.objects import Page
from pyphluence.utils import ConfluenceConfig


class MockApiCaller:
    page_data = {
        "id": "11370497",
        "type": "page",
        "status": "current",
        "title": "new page",
        "space": {
            "id": 65541,
            "key": "WC",
            "name": "Whiskey Collection",
            "type": "global",
            "status": "current",
            "_expandable": {
                "settings": "/rest/api/space/WC/settings",
                "metadata": "",
                "operations": "",
                "lookAndFeel": "/rest/api/settings/lookandfeel?spaceKey=WC",
                "identifiers": "",
                "permissions": "",
                "icon": "",
                "description": "",
                "theme": "/rest/api/space/WC/theme",
                "history": "",
                "homepage": "/rest/api/content/65625"
            },
            "_links": {
                "webui": "/spaces/WC",
                "self": "https://diditmedia.atlassian.net/wiki/rest/api/space/WC"
            }
        },
        "version": {
            "by": {
                "type": "known",
                "accountId": "557058:33b3022d-ff0d-4662-91a7-7133c7b2bb7b",
                "accountType": "atlassian",
                "email": "pmulgrew@live.com",
                "publicName": "pmulgrew",
                "profilePicture": {
                    "path": "/wiki/aa-avatar/557058:33b3022d-ff0d-4662-91a7-7133c7b2bb7b",
                    "width": 48,
                    "height": 48,
                    "isDefault": False
                },
                "displayName": "Paul Mulgrew",
                "isExternalCollaborator": False,
                "_expandable": {
                    "operations": "",
                    "personalSpace": ""
                },
                "_links": {
                    "self": "https://diditmedia.atlassian.net/wiki/rest/api/user?accountId=557058:33b3022d-ff0d-4662-91a7-7133c7b2bb7b"
                }
            },
            "when": "2023-07-06T00:53:41.898Z",
            "friendlyWhen": "Jul 05, 2023",
            "message": "",
            "number": 1,
            "minorEdit": False,
            "ncsStepVersion": "19",
            "ncsStepVersionSource": "ncs-ack",
            "confRev": "confluence$content$11370497.9",
            "contentTypeModified": False,
            "_expandable": {
                "collaborators": "",
                "content": "/rest/api/content/11370497"
            },
            "_links": {
                "self": "https://diditmedia.atlassian.net/wiki/rest/api/content/11370497/version/1"
            }
        },
        "ancestors": [
            {
                "id": "65625",
                "type": "page",
                "status": "current",
                "title": "Whiskey Collection",
                "macroRenderedOutput": {},
                "extensions": {
                    "position": 394
                },
                "_expandable": {
                    "container": "/rest/api/space/WC",
                    "metadata": "",
                    "restrictions": "/rest/api/content/65625/restriction/byOperation",
                    "history": "/rest/api/content/65625/history",
                    "body": "",
                    "version": "",
                    "descendants": "/rest/api/content/65625/descendant",
                    "space": "/rest/api/space/WC",
                    "childTypes": "",
                    "schedulePublishInfo": "",
                    "operations": "",
                    "schedulePublishDate": "",
                    "children": "/rest/api/content/65625/child",
                    "ancestors": ""
                },
                "_links": {
                    "self": "https://diditmedia.atlassian.net/wiki/rest/api/content/65625",
                    "tinyui": "/x/WQAB",
                    "editui": "/pages/resumedraft.action?draftId=65625",
                    "webui": "/spaces/WC/overview"
                }
            }
        ],
        "macroRenderedOutput": {},
        "body": {
            "storage": {
                "value": "<p>all kinds of stuff</p>",
                "representation": "storage",
                "embeddedContent": [],
                "_expandable": {
                    "content": "/rest/api/content/11370497"
                }
            },
            "_expandable": {
                "editor": "",
                "atlas_doc_format": "",
                "view": "",
                "export_view": "",
                "styled_view": "",
                "dynamic": "",
                "editor2": "",
                "anonymous_export_view": ""
            }
        },
        "metadata": {
            "labels": {
                "results": [
                    {
                        "prefix": "global",
                        "name": "test",
                        "id": "11927553",
                        "label": "test"
                    },
                    {
                        "prefix": "global",
                        "name": "new-label",
                        "id": "11960321",
                        "label": "new-label"
                    }
                ],
                "start": 0,
                "limit": 200,
                "size": 2,
                "_links": {
                    "next": "/rest/api/content/11370497/label?next=true&limit=200&start=200",
                    "self": "https://diditmedia.atlassian.net/wiki/rest/api/content/11370497/label"
                }
            },
            "_expandable": {
                "currentuser": "",
                "comments": "",
                "sourceTemplateEntityId": "",
                "simple": "",
                "properties": "",
                "frontend": "",
                "likes": ""
            }
        },
        "extensions": {
            "position": 2357
        },
        "_expandable": {
            "childTypes": "",
            "container": "/rest/api/space/WC",
            "schedulePublishInfo": "",
            "operations": "",
            "schedulePublishDate": "",
            "children": "/rest/api/content/11370497/child",
            "restrictions": "/rest/api/content/11370497/restriction/byOperation",
            "history": "/rest/api/content/11370497/history",
            "ancestors": "",
            "descendants": "/rest/api/content/11370497/descendant"
        },
        "_links": {
            "editui": "/pages/resumedraft.action?draftId=11370497",
            "webui": "/spaces/WC/pages/11370497/new+page",
            "context": "/wiki",
            "self": "https://diditmedia.atlassian.net/wiki/rest/api/content/11370497",
            "tinyui": "/x/AYCt",
            "collection": "/rest/api/content",
            "base": "https://diditmedia.atlassian.net/wiki"
        }
    }

    def get(self, api_endpoint: str, params: dict = None):
        return ApiResponse(status_code=200, data=self.page_data)


def get_api_caller():
    config = ConfluenceConfig()
    config_section = 'DEFAULT'
    base_url = config.get('base_url', config_section)
    token = config.get('token', config_section)
    username = config.get('username', config_section)

    api_caller = ApiCaller(base_url=base_url, token=token, username=username)

    return api_caller


def get_mock_page():

    page = Page(api_caller=get_api_caller())
    page.id = 123456
    page.title = 'Mock Page'
    page.body = 'Mock Body'
    page.space = 'Mock'
    page.version = 1
    page.parent = 654321


class TestPage(unittest.TestCase):
    test_page_id = 11370497

    def test_expands(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        self.assertEqual(page._expands, ['body.storage', 'space', 'version', 'ancestors', 'metadata.labels'])

    def test_add_expand(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.add_expand('body.view')
        self.assertEqual(page._expands, ['body.storage', 'space', 'version', 'ancestors', 'metadata.labels', 'body.view'])

    def test_add_expand_duplicate(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.add_expand('body.storage')
        self.assertEqual(page._expands, ['body.storage', 'space', 'version', 'ancestors', 'metadata.labels'])

    def test_remove_expand(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.add_expand('body.view')
        page.remove_expand('body.view')
        self.assertEqual(page._expands, ['body.storage', 'space', 'version', 'ancestors', 'metadata.labels'])

    def test_update_endpoints(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = 123
        self.assertEqual(page._api_endpoints['get'], '/rest/api/content/123')
        self.assertEqual(page._api_endpoints['update'], '/rest/api/content/123')
        self.assertEqual(page._api_endpoints['delete'], '/rest/api/content/123')

    def test_get(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = self.test_page_id
        page.get()
        self.assertEqual(page.status_code, 200)

    def test_404(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = 1
        page.get()
        self.assertEqual(page.status_code, 404)

    def test_get_has_space(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = self.test_page_id
        page.get()
        self.assertIn('space', page._data)

    def test_get_has_version(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = self.test_page_id
        page.get()
        self.assertIn('version', page._data)

    def test_get_has_ancestors(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = self.test_page_id
        page.get()
        self.assertIn('ancestors', page._data)

    def test_get_has_body_storage(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = self.test_page_id
        page.get()
        self.assertIn('body', page._data)
        self.assertIn('storage', page._data['body'])

    def test_get_with_no_id(self):
        with self.assertRaises(PyfluenceIDNotSetException):
            api_caller = get_api_caller()
            page = Page(api_caller)
            page.get()

    def test_get_404(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = 1
        page.get()
        self.assertEqual(page.status_code, 404)

    def test_get_has_errors(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = 1
        page.get()
        self.assertEqual(True, page.has_errors)

    def test_get_has_error_msg(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = 1
        page.get()
        self.assertIn('Not Found', page.error)

    @mock.patch('pyfluence.http.ApiCaller', side_effect=MockApiCaller)
    def test_page_title(self, MockApiCaller):
        api_caller = MockApiCaller()
        page = Page(api_caller)
        page.id = self.test_page_id
        page.get()
        self.assertEqual(page.title, 'new page')

    @mock.patch('pyfluence.http.ApiCaller', side_effect=MockApiCaller)
    def test_page_body(self, MockApiCaller):
        api_caller = MockApiCaller()
        page = Page(api_caller)
        page.id = self.test_page_id
        page.get()
        self.assertEqual(page.body, '<p>all kinds of stuff</p>')

    @mock.patch('pyfluence.http.ApiCaller', side_effect=MockApiCaller)
    def test_body_wrong_representation_exception(self, MockApiCaller):
        api_caller = MockApiCaller()
        page = Page(api_caller)
        page.id = self.test_page_id
        page.get()
        self.assertIsNone(page.get_body_representation('wrong_representation'))

    def test_body_fetch_representation(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = self.test_page_id
        page.get()
        page.get_body_representation('view')
        self.assertEqual(page._expands, ['body.storage', 'space', 'version', 'ancestors', 'metadata.labels', 'body.view'])

    @mock.patch('pyfluence.http.ApiCaller', side_effect=MockApiCaller)
    def test_url(self, MockApiCaller):
        api_caller = MockApiCaller()
        page = Page(api_caller)
        page.id = self.test_page_id
        page.get()
        self.assertEqual(page.url, 'https://diditmedia.atlassian.net/wiki/spaces/WC/pages/11370497/new+page')

    @mock.patch('pyfluence.http.ApiCaller', side_effect=MockApiCaller)
    def test_labels(self, MockApiCaller):
        api_caller = MockApiCaller()
        page = Page(api_caller)
        page.id = self.test_page_id
        page.get()
        self.assertEqual(page.labels(), ['test', 'new-label'])

    def test_add_label(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = self.test_page_id
        page.get()
        page.add_label('unittest')
        page.add_label('unittest2')
        page.add_label('unittest3')
        page.get()
        self.assertIn('unittest', page.labels())
        self.assertIn('unittest2', page.labels())
        self.assertIn('unittest3', page.labels())

    def test_remove_label(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = self.test_page_id
        page.get()
        page.remove_label('unittest')
        page.get()
        self.assertIn('unittest2', page.labels())
        self.assertIn('unittest3', page.labels())

    def test_remove_labels_all(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = self.test_page_id
        page.get()
        page.remove_all_labels()
        page.get()
        self.assertEqual(page.labels(), [])

    def test_get_parent(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = self.test_page_id
        page.get()
        parent = page.parent
        self.assertEqual(parent.id, 65625)

    def test_get_parent_none(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = 65625
        page.get()
        parent = page.parent
        self.assertIsNone(parent)

    def test_set_parent_id(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = self.test_page_id
        page.parent_id = 65625
        parent = page.parent
        self.assertEqual(parent.id, 65625)

    def test_set_parent_page(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = self.test_page_id
        parent = Page(api_caller)
        parent.id = 65625
        page.parent = parent
        parent = page.parent
        self.assertEqual(parent.id, 65625)

    def test_set_body(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.id = self.test_page_id
        page.body = '<p>new body</p>'
        self.assertEqual(page._data['body']['storage']['value'], '<p>new body</p>')

    def test_save_delete_new_page(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.title = 'new title'
        page.space_key = 'WC'
        page.body = '<p>new body</p>'
        page.parent = 65625
        page.save()
        self.assertEqual(page.has_errors, False)
        self.assertEqual(page.status_code, 200)
        self.assertIsNotNone(page.id)

        page.delete()

        self.assertEqual(page.has_errors, False)
        self.assertEqual(page.status_code, 200)
        self.assertEqual(page.id, None)
        self.assertEqual(page._data, {})

    def test_update_page(self):
        api_caller = get_api_caller()
        page = Page(api_caller)
        page.title = 'update test'
        page.body = '<p>new body</p>'
        page.space_key = 'WC'
        page.parent = 65625
        page.save()

        self.assertEqual(page.has_errors, False)
        self.assertEqual(page.status_code, 200)
        self.assertEqual(page.title, 'update test')
        self.assertEqual(page.body, '<p>new body</p>')

        page.title = 'new updated title'
        page.body = '<p>new updated body</p>'
        page.save()
        print(page.error)
        self.assertEqual(page.has_errors, False)
        self.assertEqual(page.status_code, 200)
        self.assertEqual(page.title, 'new updated title')
        self.assertEqual(page.body, '<p>new updated body</p>')
        self.assertEqual(page.version, 2)

        page.delete()

        self.assertEqual(page.has_errors, False)
        self.assertEqual(page.status_code, 200)
        self.assertEqual(page.id, None)
        self.assertEqual(page._data, {})


if __name__ == '__main__':
    unittest.main()
