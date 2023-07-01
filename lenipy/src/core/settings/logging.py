"""static methode function & constants
"""
import logging
from pydantic import BaseSettings, Field

__config = None
__command_arguments_parsed = False


class Configuration(BaseSettings):
    default_level: int = Field(logging.INFO)
    logger_configuration_path: str = Field("/app/logger/loggers.yml")
    output_directory: str = Field("/var/log/leni-py/")

    class Config:
        env_prefix = "logging_"
        env_file = "/app/env/logging_configuration.env"
        env_file_encoding = "utf-8"


def get_config() -> Configuration:
    """

    :rtype: Configuration
    :return: logging confing
    """
    global __config

    if __command_arguments_parsed:

        return __config
    else:
        __config = Configuration()
        return __config
