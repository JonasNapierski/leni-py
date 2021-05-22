import importlib
from io import FileIO
import json
import os

class Module():
    module_name=""
    module_path=""

    mainFile=""
    mainFileName=""

    request_pattern=[]


    
    def __init__(self, module_name, module_path):
        self.module_name = module_name
        self.module_path = module_path
        self.load()

    def loadConfig(self):
        tmp = self.getConfig()
        
        self.mainFileName = tmp['main']
        self.mainFile = f"{self.module_path}/{tmp['main']}"

    def getConfig(self):
       with open(f"{self.module_path}/module.json", "r") as file:
            return json.loads(file.read()) 
            file.close()

    def loadFromPathConfig(self, module_config_path):
        with open(module_config_path, "r") as file:
            return json.loads(file.read())
            file.close()

    def loadModule(self):
        self.module = importlib.import_module(f"modules.{self.module_name}.{self.mainFileName}")
    
    def load(self):
        self.loadConfig()
        self.loadModule()

    def exec(self, msg, user):
        importlib.reload(self.module)
        return self.module.exec(msg, user)