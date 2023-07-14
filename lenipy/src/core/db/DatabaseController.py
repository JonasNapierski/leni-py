import os 
import logging
from BaseDriver import BaseDriver
from driver.Pocketbase import PocketbaseDriver
from lenipy.src.core.modules.Module import Module
from lenipy.src.core.models.response import ResponseCode

log = logging.getLogger("leni.db.controller")


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

    def __get_selected_db_driver(self) -> BaseDriver or None:
        """Tries to initilize the Driver, that is selected by the env variable
        $DB_DRIVER.
        :return: Returns a child of the BaseDriver
        :rtype: BaseDriver or None
        """
        env_driver = os.getenv("DB_DRIVER")

        if env_driver is None:
            return

        if env_driver == "PocketBase":
            env_username = os.getenv("DB_USERNAME")
            env_password = os.getenv("DB_PASSWORD")
            env_url = os.getenv("DB_PB_URL")

            if env_url is None or \
                    env_password is None or \
                    env_username is None:
                log.info("You selected the Pocketbase database. Please make\
                        sure to the all the necessary")
                log.info("DB_USERNAME, DB_PASSWORD and DB_PB_URL to establish\
                        a connection to the Database.")
            driver_pb = PocketbaseDriver(user=env_username,
                                         password=env_password,
                                         url=env_url)
            if driver_pb is None:
                log.warn("Something went wrong during the Connection Process.")
            return driver_pb
