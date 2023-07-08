from BaseDriver import BaseDriver
from driver.Pocketbase import PocketbaseDriver
from lenipy.src.core.modules.Module import Module
from lenipy.src.core.models.response import ResponseCode


class DatabaseController:
    """ For more complex tasks the controller will support a high
    level function. Aswell the pursopse is that the end useres can
    just request a db object and execute the requested object.
    """

    def __init__(self):
        pass

    def init_module_config(mod: Module) -> ResponseCode:
        """Initialize the configuration of the module. This includes for
        exmaple loading the configuration and parsing the data of the config
        file to be used inside the db.
        """

        return ResponseCode(code=200)
