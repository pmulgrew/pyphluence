class BaseURLNotSetException(Exception):
    pass


class PyfluenceConfigFileNotFound(Exception):
    """
    exception for when the config file can't be found
    """
    pass


class PyfluenceConfigKeyNotFound(Exception):
    """
    exception for when the config key can't be found
    """
    pass


class PyfluenceConfigSectionNotFound(Exception):
    """
    exception for when the config section can't be found
    """
    pass


class PyfluenceIDNotSetException(Exception):
    """
    exception for when ID is not set when getting data form the server
    """
    pass
