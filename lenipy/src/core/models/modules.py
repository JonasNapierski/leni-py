"""Data class for the database model for more reference see
[here](https://github.com/jonasnapierski/leni-py/issues/27)
"""
from pydantic import BaseModel


class Modules(BaseModel):
    """
    :param str: mod_id unique identifier for module.
    :param str: name name of the module.
    :param str: url git url for the modules which should be installed.
    """
    mod_id: str
    name: str
    url: str


class ModuleConfig(BaseModel):
    """
    :param str: mod_id unique identifier of the module
    :param str: user_id unique identifier of the user
    :param str: field name of the configuration value. This will show up inside the configuration menu
    :param str: value configuration value constrained to the user and module
    """
    mod_id: str
    user_id: str
    field: str
    value: str


class ModuleCommand(BaseModel):
    """
    :param str: mod_id unique module identifier
    :param str: cmd_id id used to find the example connected to the command
    :param str: command command that will be executed by the module
    """
    mod_id: str
    cmd_id: str
    command: str


class CommandExample(BaseModel):
    """
    :param str: cmd_id used to connect to module command
    :param str: example an example for the command
    """
    cmd_id: str
    example: str
