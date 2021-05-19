import datetime
from uuid import  uuid4
import json

class TokenManager():
    
    path= ""

    def __init__(self, path):
        self.path = path
        self.tokens = []

    def getToken(self, tokenid):
        pass
    
    def  saveTokens(self):
        with open(self.path, "w") as f:
            f.write(json.dumps(self.tokens).toString())

    def create(self, userid ,activetime ):
        tk = Token()
        tk.create(userid,  datetime.datetime.now().timestamp() + activetime)
        
        self.tokens.append(tk)

        return tk

    def getTokens(self):
        return self.tokens


class Token():

    userid=""
    timestamp=None
    
    name=""

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



tm = TokenManager("./tokens.josn")
tk =tm.create("uuuu-uuuuu-uuuuu-uuuu", -60*10)
print(tk.toJSON())

tm.saveTokens()
for m in tm.tokens:
    print(m.isActive())