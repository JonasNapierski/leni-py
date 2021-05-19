import datetime
from uuid import  uuid4
import json
from dataclasses import dataclass

class TokenManager():
    
    path= ""
    tokens= []
    def __init__(self, path):
        self.path = path
        self.tokens = []
    
    def getTokenByUser(self, userid):
        for t in self.tokens:
            if t.userid == userid:
                return t

    def getTokenById(self, tokenid):
        for t in self.tokens:
            if t.name == tokenid:
                return t

    def  saveTokens(self):
        with open(self.path, "w") as f:
            a = []
            for t in self.tokens:
                temp = { "userid":  t.userid, "timestamp": t.timestamp, "name": t.name}

                a.append(json.dumps(temp))

            f.write(json.dumps(a))

    def create(self, userid ,activetime ):
        tk = Token()
        tk.create(userid,  datetime.datetime.now().timestamp() + activetime)
        
        self.tokens.append(tk.tokenData)

        return tk

    def getTokens(self):
        return self.tokens

@dataclass(frozen=True, order=True)

class TokenData:
    userid: str
    timestamp: int
    name: str

class Token():

    tokenData = None

    def __init__(self, tokenData=None):
        self.tokenData = tokenData

    def create(self, userid, expires):
        """
        userid: str ; ID of the User
        expires: int; time added from current time in seconds
        """
        self.tokenData = TokenData(userid, datetime.datetime.fromtimestamp(expires).isoformat(), uuid4().__str__())

    def isActive(self):
        if datetime.datetime.now().timestamp() <= datetime.datetime.fromisoformat(self.tokenData.timestamp).timestamp():
            return True
        return False

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
