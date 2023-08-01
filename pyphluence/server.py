from . import logger
from .utils import ConfluenceConfig
from .http import ApiCaller
from .objects import Page, Space


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
        :return: pyphluence.objects.Page
        """

        page = Page(self._api_caller)
        page.id = page_id
        page.get()
        return page

    def get_space(self, space_key: str):
        """
        Gets a space by its key
        :param space_key: str
        :return: pyphluence.objects.Space
        """

        space = Space(self._api_caller)
        space.key = space_key
        space.get()
        return space

    def create_space(self, name: str, space_key: str, description: str = None):
        """
        Creates a new space
        :param name:
        :param description:
        :param space_key: str
        :return: pyphluence.objects.Space
        """

        space = Space(self._api_caller)
        space.key = space_key
        space.name = name
        if description is not None:
            space.description = description
        space.save()
        return space


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
