from . import logger
from .utils import ConfluenceConfig
from .http import ApiCaller
from .objects import Page


class ConfluenceServer:
    """
    This class is used to interact with a Confluence Server API
    """
    def __init__(self, api_caller: ApiCaller):
        self._api_caller = api_caller

    def get_page(self, page_id: int):
        """
        Gets a page by its ID
        :param page_id: int
        :return: pyfluence.objects.Page
        """

        page = Page(self._api_caller)
        page.id = page_id
        page.get()
        return page


def connect(config_section=None) -> ConfluenceServer:
    logger.info("Connecting to Confluence")

    if config_section is None:
        logger.critical("No config section provided")
        raise Exception("No confluence config provided")

    config = ConfluenceConfig()

    base_url = config.get('base_url', config_section)
    token = config.get('token', config_section)
    username = config.get('username', config_section)

    api_caller = ApiCaller(base_url=base_url, token=token, username=username)

    server = ConfluenceServer(api_caller=api_caller)

    return server
