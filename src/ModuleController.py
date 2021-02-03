from glob import glob

from src.Module import Module


class ModuleController():
    module_names = []
    modules= []
    def __init__(self, module_path):
        self.module_path = module_path
    
    def find_all_files(self):
        self.module_names = glob(f"{self.module_path}/*")

        for i in range(0, len(self.module_names)):
            self.module_names[i] = self.module_names[i].replace(f"{self.module_path}\\", "")
        return self.module_names

    def load_all_module(self):
        if self.module_names == None :
            self.find_all_files()

        for name in self.module_names:
            self.modules.append(self.load_module(name))

    def load_module(self, name):
        return Module(name, f"{self.module_path}/{name}")

