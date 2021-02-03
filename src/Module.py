import importlib
from io import FileIO
import json
import os

class Module():
    def __init__(self, module_name, module_path):
        self.module_name = module_name
        self.module_path = module_path
        self.load()

    def loadConfig(self):
        with open(f"{self.module_path}\\module.json", "r") as file:
            tmp = json.loads(file.read())
        
        self.mainFileName = tmp['main']
        self.mainFile = f"{self.module_path}/{tmp['main']}"

    def loadModule(self):
        self.module = importlib.import_module(f"module.{self.module_name}.{self.mainFileName}")
    
    def load(self):
        self.loadConfig()
        self.loadModule()

    def exec(self):
        importlib.reload(self.module)
        self.module.init()
