import unittest
from pyfluence import server
from pyfluence.objects import Page
from pyfluence.exceptions import PyfluenceConfigSectionNotFound


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


if __name__ == '__main__':
    unittest.main()
