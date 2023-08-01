import unittest
from pyphluence import server
from pyphluence.objects import Page
from pyphluence.exceptions import PyfluenceConfigSectionNotFound


class TestServer(unittest.TestCase):
    test_page_id = 65625

    def test_no_config(self):
        with self.assertRaises(Exception):
            server.connect()

    def test_connect(self):
        s = server.connect('DEFAULT')
        self.assertIsInstance(s, server.ConfluenceServer)

    def test_wrong_config(self):
        with self.assertRaises(PyfluenceConfigSectionNotFound):
            server.connect('WRONG')

    def test_get_page(self):
        s = server.connect('DEFAULT')
        page = s.get_page(self.test_page_id)
        self.assertEqual(page.id, self.test_page_id)
        self.assertIsInstance(page, Page)

    def test_create_space(self):
        s = server.connect('DEFAULT')
        space = s.create_space('Test space', 'abc')
        self.assertEqual(space.key, 'abc')
        self.assertEqual(space.name, 'Test space')
        self.assertEqual(space.description, '')
        space.delete()

    def test_get_space(self):
        s = server.connect('DEFAULT')
        space = s.get_space('test')
        self.assertEqual(space.key, 'test')
        self.assertEqual(space.name, 'test')
        self.assertEqual(space.description, '')


if __name__ == '__main__':
    unittest.main()
