from typing import List
from pocketbase import PocketBase
from lenipy.src.core.db.BaseDriver import BaseDriver
from lenipy.src.core.models.modules import Modules, ModuleConfig, ModuleCommand, CommandExample


class PocketbaseDriver(BaseDriver):

    def __init__(self, user, password, url):
        self.client: PocketBase = PocketBase(url)
        self.admin = self.client.admins.auth_with_password(user, password)

    def connect(self):
        pass

    def create_modules(self, modules: Modules):
        self.client.collection("modules").create(
                {
                    "url": modules.url,
                    "name": modules.name
                }
                )

    def get_modules_list(self):
        pb_list_record = self.client.collection("modules").get_full_list()
        modules = []
        for module_record in pb_list_record:
            modules.append(Modules(
                    mod_id=module_record.id,
                    name=module_record.name,
                    url=module_record.url
                ))
        return modules

    def get_modules_by_id(self, mod_id: str) -> Modules:
        module_raw = self.client.collection("modules").get_one(mod_id)

        data_mod_id = module_raw.id
        data_name = module_raw.name
        data_url = module_raw.url

        return Modules(mod_id=data_mod_id,
                       name=data_name,
                       url=data_url)

    def create_mod_config(self, mod_config: ModuleConfig):
        self.client.collection("mod_config").create(
                {
                    "mod_id": mod_config.mod_id,
                    "user_id": mod_config.user_id,
                    "field": mod_config.field,
                    "value": mod_config.value
                })

    def get_mod_config_list(self) -> List[ModuleConfig]:
        pb_mod_configs = self.client.collection("mod_config").get_full_list()
        mod_configs = []
        for mod_config in pb_mod_configs:
            mod_configs.append(ModuleConfig(
                    mod_id=mod_config.id,
                    user_id=mod_config.user_id,
                    field=mod_config.field,
                    value=mod_config.value
                ))
        return mod_configs

    def get_mod_config_by_field(self, mod_id: str,
                                mod_field: str) -> (ModuleConfig or None):
        resp_mod_config = None
        for mod_config in self.get_mod_config_list():
            if mod_config.mod_id == mod_id and \
               mod_config.field.lower() == mod_field.lower():
                resp_mod_config = mod_config
                break
        return resp_mod_config

    def create_mod_command(self, mod_command: ModuleCommand):
        self.client.collection("mod_commands").create(
                {
                    "mod_id": mod_command.mod_id,
                    "command": mod_command.command
                })

    def get_mod_command_list(self):
        pb_mod_cmds = self.client.collection("mod_commands").get_full_list()

        mod_commands = []
        for mod_command in pb_mod_cmds:
            mod_commands.append(ModuleCommand(
                    mod_id=mod_command.id,
                    cmd_id=mod_command.cmd_id,
                    command=mod_command.command
                ))
        return mod_commands

    def get_mod_command_by_command(self,
                                   mod_id: str,
                                   command: str) -> (ModuleCommand or None):
        mod_commands = self.get_mod_config_list()

        resp_mod_command = None

        for mod_command in mod_commands:
            if mod_command.mod_id == mod_id and \
               mod_command.command == command:
                resp_mod_command = mod_command
        return resp_mod_command

    def create_command_example(self, cmd_example: CommandExample):
        self.client.collection("cmd_examples").create(
                {
                    "example": cmd_example
                })

    def get_command_example_list(self):
        pb_cmd_exmaple = self.client.collection("cmd_examples").get_full_list()
        resp_cmd_exmaple = []
        for cmd_exmaple in pb_cmd_exmaple:
            resp_cmd_exmaple.append(CommandExample(
                    cmd_id=cmd_exmaple.id,
                    example=cmd_exmaple.example
                ))
        return resp_cmd_exmaple

    def get_command_example_by_cmd(self, cmd_id: str) -> List[CommandExample]:
        cmd_exmaples = self.get_command_example_list()
        return [e for e in cmd_exmaples if e.cmd_id == cmd_id]
