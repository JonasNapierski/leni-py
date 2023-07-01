import logging
import os
from lenipy.src.core.settings.logging import get_config


def test_empty_config():
    log_conf = get_config()

    assert log_conf.default_level == logging.INFO
    assert log_conf.logger_configuration_path == "/app/logger/loggers.yml"
    assert log_conf.output_directory == "/var/log/leni-py/"


def test_command_loaded_config():
    pass


def test_environment_loaded_config():
    os.environ["logging_defaul_level"] = "0"
    os.environ["logging_logger_configuration_path"] = "/"
    os.environ["logging_output_directory"] = "/"

    log_conf = get_config()
    log_conf._iter
    assert log_conf.default_level == 0
    assert log_conf.logger_configuration_path == "/"
    assert log_conf.output_directory == "/"
