import os
import datetime
from uuid import  uuid4
import json

class TokenManager():
    
    path= ""
    tokens= []

    def __init__(self, path):
        self.path = path


    def loadTokens(self):
        pass


    def loadToken(self, filepath):
        with open(filepath, "r")
    def saveTokens(self):
        with open(self.path, "w") as file:
            file.write(json.dump(self.tokens))
            file.close()

    def getToken(self, tokenid):
        pass

    def getTokens(self):
        return self.tokens




class Token():

    userid=""
    timestamp=None
    
    name=""

    def load(self, name, timestamp, userid):
        self.name = name
        self.timestamp = timestamp
        self.userid = userid

    def __init__(self):
        pass

    def create(self, userid, expires):
        self.userid = userid
        self.name = uuid4().__str__()
        self.timestamp = datetime.datetime.fromtimestamp(expires).isoformat()

    def isActive(self):
        if datetime.datetime.now().timestamp() <= datetime.datetime.fromisoformat(self.timestamp).timestamp():
            return True
        return False

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

