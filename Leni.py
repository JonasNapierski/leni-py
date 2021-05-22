import os 
from src.modules.Module import Module
from src.modules.ModuleController import ModuleController
from src.user.UserManager import  UserManager
from src.tokens.TokenManager import *
from flask import Flask, Request, jsonify, render_template, request
from  src.ai.AI import Training
from src.user.User import User
import json
import requests


app = Flask(__name__)

with open("./config.json", "r") as f:
    cfg = json.loads(f.read())

HOST=cfg['host']
PORT=cfg['port']



# bot.add(["hi", "hello", "welcome", "tach", "guten morgen", "guten tag"] ,"morning")
# bot.add(["cia", "tschüss", "bye", "bis bald"],"goodbye")
# bot.filter([".","!","?"])

# bot.create_set()
# bot.train(num_epochs=5000, batch_size=8, learning_rate=0.001, hidden_size=8, num_workers=0, FILE_PATH="DATA.pth")

bot = Training()
mc = ModuleController("./modules")
mc.module_names = []
mc.find_all_files()
mc.load_all_module()

bot.load(FILE_PATH="DATA.pth")
bot.print()
for m in mc.modules:
    mcfg = m.getConfig()
    bot.add(mcfg[cfg['language']], m.module_name)

#bot.create_set()
#bot.train(num_epochs=5000, batch_size=8, learning_rate=0.001, hidden_size=8, num_workers=0, FILE_PATH="DATA.pth")

bot.load(FILE_PATH="DATA.pth")
bot.print() 


userManager = UserManager("./data/")

users = userManager.get_users()

 # init and load tokens 

tokenManager = TokenManager(cfg['token_file'])
tokenManager.loadTokens()

tmp = None
for tokendata in tokenManager.tokens:
    print(f"Add {tokendata.name} to {tokendata.userid}")
    userManager.add_token(tokendata.userid, tokendata)

for user in users:
    for module in mc.modules:
        user.copy_config(module.module_name, module.getConfig())






def check_for_token(param):
    if param == None:
        return False
    
    if tokenManager.__contains__(param['key']) and  Token(tokenManager.getTokenById(param['key'])).isActive():
        return True
    return False


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")
    

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

@app.route("/api/modules", methods=['GET'])
def list_all_module():
    if check_for_token(request.args):
        return jsonify("INVALID API KEY")

    mm = []

    for m in mc.modules:
        mm.append(m.module_name)

    return jsonify(mm)
    

@app.route("/api/module/<module>", methods=['GET'])
def list_module(module):
    if not check_for_token(request.args):
        return jsonify("INVALID API KEY")

    print(module)
    for m in mc.modules:
        if m.module_name == str(module):
            return jsonify(m.exec(""))

@app.route("/api/process", methods=["POST"])
def process():
    if not check_for_token(request.args):
        return jsonify("INVALID API KEY")

    data = request.json
    msg = data['msg']
    
    (module, weight) = bot.process(msg)
    
    print(f"{module}:{weight:.4f}")
    for m in mc.modules:
        
        if str(m.module_name) == str(module):
            if request.is_json:
                user = userManager.get_user(tokenManager.getTokenById(request.args['key']).userid)
                if user == None:
                    return jsonify("USER NOT FOUND BY TOKEN")
                return jsonify(m.exec(msg, user))
    return jsonify(data)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=False)
