import unittest
from pyphluence.utils import ConfluenceConfig
from pyphluence.exceptions import PyfluenceConfigFileNotFound, PyfluenceConfigSectionNotFound, PyfluenceConfigKeyNotFound
from pathlib import Path


class TestConfig(unittest.TestCase):
    def test_config_not_found(self):
        with self.assertRaises(PyfluenceConfigFileNotFound):
            ConfluenceConfig('noconfig.cfg', '.pyfluence', False)

    def test_config_file(self):
        config = ConfluenceConfig()
        self.assertEqual(config._config_file, 'config.cfg')

    def test_config_key_not_found(self):
        config = ConfluenceConfig(config_file="config.cfg", config_path="tests/.pyphluence", config_in_home=False)
        with self.assertRaises(PyfluenceConfigKeyNotFound):
            config.get('test', 'DEFAULT')

    def test_config_key_found(self):
        config = ConfluenceConfig(config_file="config.cfg", config_path="tests/.pyphluence", config_in_home=False)
        self.assertEqual(config.get('name', 'DEFAULT'), 'pyphluence')

    def test_config_key_found2(self):
        config = ConfluenceConfig(config_file="config.cfg", config_path="tests/.pyphluence", config_in_home=False)
        self.assertEqual(config.get('version', 'DEFAULT'), '0.1.0')


if __name__ == '__main__':
    unittest.main()
