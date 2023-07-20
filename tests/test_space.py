import unittest

from pyfluence.exceptions import PyfluenceIDNotSetException
from pyfluence.objects import Space, Page
from pyfluence.utils import ConfluenceConfig
from pyfluence.http import ApiCaller


def get_api_caller():
    config = ConfluenceConfig()
    config_section = 'DEFAULT'
    base_url = config.get('base_url', config_section)
    token = config.get('token', config_section)
    username = config.get('username', config_section)

    api_caller = ApiCaller(base_url=base_url, token=token, username=username)

    return api_caller


class TestSpace(unittest.TestCase):
    test_page_id = 65625

    def test_get_page(self):
        s = Space(get_api_caller())
        s.key = 'WC'
        page = s.get_page(self.test_page_id)
        self.assertIsInstance(page, Page)

    def test_get_page_raises_no_space_data(self):
        s = Space(get_api_caller())
        with self.assertRaises(ValueError):
            s.get_page(self.test_page_id)

    def test_get_page_space_doesnt_exist(self):
        s = Space(get_api_caller())
        s.key = 'WRONG'
        with self.assertRaises(ValueError):
            s.get_page(self.test_page_id)

    def test_page_exists_but_not_in_space(self):
        s = Space(get_api_caller())
        s.key = 'test'
        p = s.get_page(65625)
        self.assertEqual(p.status_code, 404)

    def test_new_page(self):
        s = Space(get_api_caller())
        s.key = 'WC'
        p = s.new_page()
        self.assertIsInstance(p, Page)
        self.assertEqual(p.space_key, s.key)

    def test_new_space(self):
        s = Space(get_api_caller())
        s.key = 'abc'
        s.name = 'Test space'
        s.save()

        self.assertEqual(s.has_errors, False)
        self.assertIsInstance(s, Space)
        self.assertEqual(s.key, 'abc')
        self.assertEqual(s.name, 'Test space')
        self.assertEqual(s.type, 'global')

        s.delete()
        self.assertEqual(s.has_errors, False)


if __name__ == '__main__':
    unittest.main()
