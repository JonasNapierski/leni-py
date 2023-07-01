"""static methode function & constants
"""
import logging
from pydantic import BaseSettings


class Configuration(BaseSettings):
    default_level: int = logging.INFO
    logger_configuration_path: str = "/app/logger/loggers.yml"
    output_directory: str = "/var/log/leni-py/"
