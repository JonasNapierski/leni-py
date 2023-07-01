from pydantic import BaseModel


class Modules(BaseModel):
    mod_id: str
    name: str
    url: str


class ModuleConfig(BaseModel):
    mod_id: str
    user_id: str
    field: str
    value: str


class ModuleCommand(BaseModel):
    mod_id: str
    cmd_id: str
    command: str


class CommandExample(BaseModel):
    cmd_id: str
    example: str
