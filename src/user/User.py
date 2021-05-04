import json 
import uuid
import os 

class User():
    path = ""
    uuid= ""
    password_hash=""
    tokens=[]

    def __init__(self, path):
        self.path = path 

    def gen_uuid(self):
        return uuid.uuid4().__str__()

    def create(self, displayname, uuid, password_hash, tokens):
        self.displayname = displayname
        self.uuid = uuid
        self.password_hash = password_hash
        self.tokens = tokens

    def load(self, file):
        with open(file, "r") as f:
            data = json.loads(f.read())
            self.create(data["displayname"], data["uuid"], data["password_hash"], [])

    
    def save_profile(self, path):
        json_data = self.toJSON()
        
        f = open(f"{path}/users/{self.uuid}.json", "w")
        f.write(json_data)
        f.close()

    def create_config_folder(self, path="./data/"):
        os.makedirs(f"{path}config/{self.uuid}")

    def copy_config(self, module_name, module_config, path="./data/"):
        if  os.path.exists(f"{path}config/{self.uuid}/{module_name}.json"):
            print(f"{path}config/{self.uuid}/{module_name}.json File already exists")
            return
        if not os.path.exists(f"{path}config/{self.uuid}"):
            os.makedirs(f"{path}config/{self.uuid}")

        with open(f"{path}config/{self.uuid}/{module_name}.json", "w+") as file_:
            if os.path.exists(f"{path}config/{self.uuid}/{module_name}.json"):
                json.dump(module_config, file_)


    def check_for_token(self, token):
        if self.tokens.__contains__(token):
            return True
        return False

    def add_token(self, token):
        self.tokens.append(token)
        self.save_profile(self.path)

    def set_tokens(self, tokens):
        self.tokens = tokens
    def load_module_config(self, module_name):
        return 

    def check_uuid(self, uuid):
        if self.uuid == uuid:
            return True
        return False

    def check_password(self, raw_hash):
        if raw_hash == self.password_hash:
            return True
        return False

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


