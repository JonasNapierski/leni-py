from glob import glob
from src.modules.Module import Module
import json
import re
import os


class ModuleController():
    module_names = []
    modules= []
    registry_file_name="module.json"

    def __init__(self, module_path):
        """
        ModuleController search in the 'module_path' for 'Modules'

        Module: A module is named after the directory it is contained.
                -> in the folder must be a module.json file!
                -> there is a main file which is register in the module.json
        """
        if not os.path.exists(module_path):
            os.makedirs(module_path)
        self.module_path = module_path
    
    def find_all_files(self):
        """
        List all directories in the Modules-folder and add them to the 'module_names'
        """
        self.module_names = []
        self.module_names = glob(f"{self.module_path}/*")

        for i in range(0, len(self.module_names)):
            self.module_names[i] = re.sub(rf'{self.module_path}(/|\\)*', '', self.module_names[i])
        return self.module_names

    def load_all_module(self) -> None:
        if self.module_names is None:
            self.find_all_files()

        if self.modules:
            return self.modules

        for name in self.module_names:
            self.modules.append(self.load_module(name))

    def load_module(self, name):
        return Module(name, f"{self.module_path}/{name}")

    def getModule(self, index):
        return self.modules[index]

    def getModuleRange(self, bottom, top):
        m_array = []
        for i in range(bottom, top):
            m_array.append(self.getModule(i))
        return m_array

    def create_register_file(self):
        with open(f"{self.module_path}/{self.registry_file_name}") as f:
            # check if File don't exists
            registry = json.loads(f.read())
            # TODO this is still in work in progress 
