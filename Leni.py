from fastapi import FastAPI
from src.modules.ModuleController import ModuleController
from src.api.request_model import RequestText
from src.Debugger import Debug
from src.ai.AI import Training
import json

app = FastAPI()

with open("./config.json", "r") as f:
    cfg = json.loads(f.read())

# init bot_module_namer and Module-Controller and feed the modules into the ai
bot_module_namer = Training("Module Namer")
bot_module_cmd_predictor = Training("Module CMD Predictor")

mc = ModuleController("./modules")
mc.find_all_files()
mc.load_all_module()


# init AI


# bot module namer && bot module command predictor
for module in mc.modules:
    tmp_arr = []
    tmp_config = module.getConfig()
    for cmd in tmp_config["commands"]:
        tmp_arr.extend(cmd["examples"])
        bot_module_cmd_predictor.add(cmd["examples"], cmd["command-name"])
    bot_module_namer.add(tmp_arr, module.module_name)

if not bot_module_namer.load(FILE_PATH="./data/ai/Module_Namer.ai"):
    bot_module_namer.filter()
    bot_module_namer.create_set()
    bot_module_namer.train(num_epochs=3000,
                           batch_size=8,
                           learning_rate=0.001,
                           hidden_size=8,
                           num_workers=0,
                           FILE_PATH="./data/ai/Module_Namer.ai")

if not bot_module_cmd_predictor.load(FILE_PATH="./data/ai/Module_Command.ai"):
    bot_module_cmd_predictor.filter()
    bot_module_cmd_predictor.create_set()
    bot_module_cmd_predictor.train(num_epochs=5000,
                                   batch_size=8,
                                   learning_rate=0.001,
                                   hidden_size=8,
                                   num_workers=0,
                                   FILE_PATH="./data/ai/Module_Command.ai")


def list_all_module():
    """list of all modules
    """
    mc.load_all_module()

    mm = []

    for m in mc.modules:
        if m not in mm:
            mm.append(m.module_name)

    return mm


@app.get("/api/modules")
def list_modules():
    return list_all_module()


@app.get("/api/module/{module}")
def list_module(module: str):
    """list a specific module for a list of the module see /api/modules

    :param module: module name to be request
    :type: str
    :rtype: Module
    :return: request something from the module
    """
    for m in mc.modules:
        if m.module_name == str(module):
            return m.exec("")
    return {"msg": "No module found", "code": 404}




@app.post("/api/process")
def process(req: RequestText):
    """processes the text request and response with the module answer

        :rtype: dict
        :return: text -> module -> response
    """
    msg = req.msg

    (module, weight) = bot_module_namer.process(msg)
    Debug.print(f"Module Namer | {module}:{weight:.4f}")

    (predicted_cmd, cmd_weight) = bot_module_cmd_predictor.process(msg)
    Debug.print(f"Module CMD Predictor | {predicted_cmd}:{cmd_weight:.4f}")

    for m in mc.modules:
        if str(m.module_name) == str(module):
            module_output = m.exec(msg, user, predicted_cmd)
            return module_output
    return {"msg": "Sorry we could not process your request", "code": 500}
