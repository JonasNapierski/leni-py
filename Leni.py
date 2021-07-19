import os 
import sys
from src.modules.Module import Module
from src.modules.ModuleController import ModuleController
from src.user.UserManager import  UserManager
from src.tokens.TokenManager import *
from src.Debugger import Debug
from src.AdminConsole import AdminConsole
from flask import Flask,  jsonify, render_template, request
from  src.ai.AI import Training
from src.user.User import User
import json
from multiprocessing import Process
from threading import Thread



with open("./config.json", "r") as f:
    cfg = json.loads(f.read())

HOST=cfg['host']
PORT=cfg['port']

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
    bot_module_namer.train(num_epochs=5000, batch_size=8,learning_rate=0.001, hidden_size=8, num_workers=0, FILE_PATH="./data/ai/Module_Namer.ai")

if not bot_module_cmd_predictor.load(FILE_PATH="./data/ai/Module_Command.ai"):
    bot_module_cmd_predictor.filter()
    bot_module_cmd_predictor.create_set()
    bot_module_cmd_predictor.train(num_epochs=5000, batch_size=8, learning_rate=0.001, hidden_size=8, num_workers=0, FILE_PATH="./data/ai/Module_Command.ai")

# init user-manager
userManager = UserManager("./data/")

# init and load tokens 
tokenManager = TokenManager(cfg['token_file'])


def load_tokens():
    tokenManager.loadTokens()
    for tokendata in tokenManager.tokens:
        Debug.print(f"Add Token: [{tokendata.name}] to user [{tokendata.userid}]")
        userManager.add_token(tokendata.userid, tokendata)

def create_user_modules():
    for user in userManager.get_users():
        for module in mc.modules:
            user.copy_config(module.module_name, module.getConfig())
    userManager.load_users()

load_tokens()
create_user_modules()

# check if the token is active and valid; will return True or False
def check_for_token(param):
    if param == None:
        return False
    
    if tokenManager.__contains__(param['key']) and  Token(tokenManager.getTokenById(param['key'])).isActive():
        return True
    return False

# init flask
app = Flask(__name__)

# index route -- temp leni design switch in future to a react framework http://github.com/jonasnapierski/leni-react-ui


# login route -- login with user and password hash to generate or get an active token
@app.route("/login", methods=["POST"])
def login_route():
    body = request.json

    if body == None:
        return
    userManager.load_users()
    user = userManager.get_user_by_name(body['username'])
    if user != None and user.check_password(body['password']):
        tmpData = Token(tokenManager.getTokenByUser(user.uuid))
        if tmpData.tokenData == None:
            tmpData = tokenManager.create(user.uuid, 60*60*24)
            userManager.add_token(body['username'], tmpData.tokenData)
            tokenManager.saveTokens()
            load_tokens()
        return jsonify({"token": tmpData.tokenData.name})
    return {"MSG":"NO VALID USER INFORMATION", "COD": 400}


# api/modules route -- get a list of all modules 
@app.route("/api/modules", methods=['GET'])
def list_all_module():

    mc.load_all_module()
    create_user_modules()

    if check_for_token(request.args):
        return jsonify({"msg":"INVALID LOGIN TOKEN", "cod": 401})

    mm = []

    for m in mc.modules:
        mm.append(m.module_name)

    return jsonify(mm)
    

# api/module/<module> route -- get a specific module 
@app.route("/api/module/<module>", methods=['GET'])
def list_module(module):
    if not check_for_token(request.args):
        return jsonify({"msg":"INVALID LOGIN TOKEN", "cod": 401})
        


    for m in mc.modules:
        if m.module_name == str(module):
            return jsonify(m.exec(""))


# api/process route -- here is where the magic happens. AI tries to figure out which module to use and pick one.
@app.route("/api/process", methods=["POST"])
def process():
    if not check_for_token(request.args):
        return jsonify({"msg":"INVALID LOGIN TOKEN", "cod": 401})
        

    data = request.json
    msg = data['msg']
    
    (module, weight) = bot_module_namer.process(msg)
    Debug.print(f"Module Namer | {module}:{weight:.4f}")

    (predicted_cmd, cmd_weight) = bot_module_cmd_predictor.process(msg)
    Debug.print(f"Module CMD Predictor | {predicted_cmd}:{cmd_weight:.4f}" )

    for m in mc.modules:
        if str(m.module_name) == str(module):
            if request.is_json:
                user = userManager.get_user(tokenManager.getTokenById(request.args['key']).userid)
                if user == None:
                    return jsonify("USER NOT FOUND BY TOKEN")
                
                if not os.path.exists(f"./data/config/{user.uuid}"):
                    create_user_modules()
                module_output = m.exec(msg, user, predicted_cmd)
                return jsonify(module_output)
    return jsonify(data)


def run_flask():
    app.run(host=HOST, port=PORT, debug=False)

def run_admin():
    adminConsole = AdminConsole(userManager, tokenManager, bot_module_namer, mc)
    adminConsole.run()
    adminConsole.input_loop()



if __name__ == "__main__":
   flaskProcess = Process(target=run_flask)
   adminProcess = Process(target=run_admin)
   flaskProcess.start()
   adminProcess.start()

   