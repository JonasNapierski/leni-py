import logging
from lenipy.src.core.settings.logging import Configuration


def test_empty_config():
    log_conf = Configuration()

    assert log_conf.default_level == logging.INFO
    assert log_conf.logger_configuration_path == "/app/logger/loggers.yml"
    assert log_conf.output_directory == "/var/log/leni-py/"


def test_command_loaded_config():
    pass


def test_environment_loaded_config():
    pass
