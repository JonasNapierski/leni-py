import os 
from src.Module import Module
from src.ModuleController import ModuleController


mc = ModuleController("./modules")
mc.find_all_files()
mc.load_all_module()
for m in mc.modules:
    m.exec("")