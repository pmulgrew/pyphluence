import configparser
from pathlib import Path
from . import logger
from .exceptions import PyfluenceConfigFileNotFound, PyfluenceConfigSectionNotFound, PyfluenceConfigKeyNotFound


class ConfluenceConfig:
    """
    ConfluenceConfig is a class that handles the configuration for pyphluence

    :param config_file: the name of the config file
    :param config_path: the path to the config file
    :param config_in_home: if the config file is in the home directory

    :type config_file: str
    :type config_path: str
    :type config_in_home: bool

    :raises PyfluenceConfigFileNotFound: if the config file is not found
    :raises PyfluenceConfigSectionNotFound: if the config section is not found
    :raises PyfluenceConfigKeyNotFound: if the config key is not found

    :return: the config object
    :rtype: configparser.ConfigParser

    """
    _config_file: str = 'config.cfg'
    _config_path: str = '.pyphluence'
    _config_in_home: bool = True

    def __init__(self, config_file: str = 'config.cfg', config_path: str = '.pyphluence', config_in_home: bool = True):
        self._config_file = config_file
        self._config_path = config_path
        self._config_in_home = config_in_home

        self._config = configparser.ConfigParser()

        self.__validate_configs()

    def get(self, config: str, section: str = 'DEFAULT'):
        """
        Gets the value from the config section
        Parameters
        ----------
        config
        section

        Raises
        -------
        PyfluenceConfigSectionNotFound
            If the config section is not found
        PyfluenceConfigKeyNotFound
            If the config key is not found
        """
        logger.debug(f"Getting config {config} from section {section}")

        if section not in self._config:
            logger.critical(f"Config section is missing {section}")
            raise PyfluenceConfigSectionNotFound(f'Config section not found: {section}')

        if config not in self._config[section]:
            logger.critical(f"Config key is missing {config}")
            raise PyfluenceConfigKeyNotFound(f'Config key not found: {config} in section: {section}')

        return self._config[section][config]

    def _build_config_path(self):

        path = Path()

        if not self._config_in_home and not self._config_path:
            path = Path().joinpath(self._config_file).resolve()

        if not self._config_in_home and self._config_path:
            path = Path().joinpath(self._config_path, self._config_file).resolve()

        if self._config_in_home and not self._config_path:
            path = Path.home().joinpath(self._config_file).resolve()

        if self._config_in_home and self._config_path:
            path = Path.home().joinpath(self._config_path, self._config_file).resolve()

        return path

    def __validate_configs(self):
        config_path = self._build_config_path()

        if not config_path.exists():
            logger.critical(f"Config file is missing {str(config_path)}")
            raise PyfluenceConfigFileNotFound(f'Config file not found: {str(config_path)}')
        else:
            self._config.read(config_path)
