import os 
import sys
from src.modules.Module import Module
from src.modules.ModuleController import ModuleController
from src.user.UserManager import  UserManager
from src.tokens.TokenManager import *
from src.Debugger import Debug
from src.AdminConsole import AdminConsole
from flask import Flask, Request, jsonify, render_template, request
from  src.ai.AI import Training
from src.user.User import User
import json
import requests
from multiprocessing import Process
from threading import Thread


app = Flask(__name__)

with open("./config.json", "r") as f:
    cfg = json.loads(f.read())

HOST=cfg['host']
PORT=cfg['port']

# init bot and Module-Controller and feed the modules into the ai
bot = Training()
mc = ModuleController("./modules")
mc.module_names = []
mc.find_all_files()
mc.load_all_module()

for m in mc.modules:
    mcfg = m.getConfig()
    bot.add(mcfg[cfg['language']], m.module_name)

bot.load(FILE_PATH="DATA.pth")

# init user-manager
userManager = UserManager("./data/")

# init and load tokens 
tokenManager = TokenManager(cfg['token_file'])
tokenManager.loadTokens()

tmp = None
for tokendata in tokenManager.tokens:
    Debug.print(f"Add Token: [{tokendata.name}] to user [{tokendata.userid}]")
    userManager.add_token(tokendata.userid, tokendata)

for user in userManager.get_users():
    for module in mc.modules:
        user.copy_config(module.module_name, module.getConfig())


# check if the token is active and valid; will return True or False
def check_for_token(param):
    if param == None:
        return False
    
    if tokenManager.__contains__(param['key']) and  Token(tokenManager.getTokenById(param['key'])).isActive():
        return True
    return False


# index route -- temp leni design switch in future to a react framework http://github.com/jonasnapierski/leni-react-ui
@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")
    

# login route -- login with user and password hash to generate or get an active token
@app.route("/login", methods=["POST"])
def login_route():
    body = request.json

    if body == None:
        return

    user = userManager.get_user_by_name(body['username'])
    if user != None and user.check_password(body['password']):
        tmpData = Token(user.get_active_token())
        if tmpData.tokenData == None:
            tmpData = tokenManager.create(user.uuid, 60*24)
            userManager.add_token(body['username'], tmpData)
            tokenManager.saveTokens()
        return jsonify({"token": tmpData.tokenData.name})
    return {"MSG":"NO VALID USER INFORMATION", "COD": 400}


# api/modules route -- get a list of all modules 
@app.route("/api/modules", methods=['GET'])
def list_all_module():
    if check_for_token(request.args):
        return jsonify("INVALID API KEY")

    mm = []

    for m in mc.modules:
        mm.append(m.module_name)

    return jsonify(mm)
    

# api/module/<module> route -- get a specific module 
@app.route("/api/module/<module>", methods=['GET'])
def list_module(module):
    if not check_for_token(request.args):
        return jsonify("INVALID API KEY")


    for m in mc.modules:
        if m.module_name == str(module):
            return jsonify(m.exec(""))


# api/process route -- here is where the magic happens. AI tries to figure out which module to use and pick one.
@app.route("/api/process", methods=["POST"])
def process():
    if not check_for_token(request.args):
        return jsonify("INVALID API KEY")

    data = request.json
    msg = data['msg']
    
    (module, weight) = bot.process(msg)
    
    Debug.print(f"{module}:{weight:.4f}")

    for m in mc.modules:
        
        if str(m.module_name) == str(module):
            if request.is_json:
                user = userManager.get_user(tokenManager.getTokenById(request.args['key']).userid)
                if user == None:
                    return jsonify("USER NOT FOUND BY TOKEN")
                return jsonify(m.exec(msg, user))
    return jsonify(data)


def run_flask():
    app.run(host=HOST, port=PORT, debug=False)

def run_admin():
    adminConsole = AdminConsole()
    adminConsole.run()
    adminConsole.input_loop()


if __name__ == "__main__":
   flaskProcess = Process(target=run_flask)
   adminProcess = Process(target=run_admin)
   flaskProcess.start()
   adminProcess.start()