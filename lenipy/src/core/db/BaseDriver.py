from lenipy.src.core.models.modules import (Modules,
                                            ModuleConfig,
                                            ModuleCommand,
                                            CommandExample)


class BaseDriver:

    def __init__():
        pass

    def connect():
        pass

    def create_modules(module: Modules):
        pass

    def get_modules_list():
        pass

    def get_modules_by_id(mod_id: str) -> Modules:
        pass

    def create_mod_config(mod_config: ModuleConfig):
        pass

    def get_mod_config_list():
        pass

    def get_mod_config_by_field(mod_id: str, mod_field: str) -> ModuleConfig:
        pass

    def create_mod_command(mod_command: ModuleCommand):
        pass

    def get_mod_command_list():
        pass

    def get_mod_command_by_command(mod_id: str, command: str):
        pass

    def create_command_example(cmd_example: CommandExample):
        pass

    def get_command_example_list():
        pass

    def get_command_example_by_example(example: str):
        pass
