from lenipy.src.core.models.modules import (Modules,
                                            ModuleConfig,
                                            ModuleCommand,
                                            CommandExample)


class BaseDriver:

    def __init__(self):
        pass

    def connect(self):
        pass

    def create_modules(self, module: Modules):
        pass

    def get_modules_list(self):
        pass

    def get_modules_by_id(self, mod_id: str) -> Modules:
        pass

    def create_mod_config(self, mod_config: ModuleConfig):
        pass

    def get_mod_config_list(self):
        pass

    def get_mod_config_by_field(self, mod_id: str, mod_field: str) -> ModuleConfig:
        pass

    def create_mod_command(self, mod_command: ModuleCommand):
        pass

    def get_mod_command_list(self):
        pass

    def get_mod_command_by_command(self, mod_id: str, command: str):
        pass

    def create_command_example(self, cmd_example: CommandExample):
        pass

    def get_command_example_list(self):
        pass

    def get_command_example_by_cmd(self, cmd_id: str):
        pass
