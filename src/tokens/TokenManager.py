import datetime
from json.decoder import JSONDecodeError
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
    
    def loadTokens(self):
        self.tokens = []
        try:
            with open(self.path, "r") as f:
                try:
                    json_ = json.loads(f.read())
                    
                    for object in json_:
                        print(object)
                        tkData = TokenData(object["userid"], object["timestamp"], object["name"])
                        self.tokens.append(tkData)
                except JSONDecodeError as e:
                    pass
        except:
            with open(self.path, "w") as f:
                f.write("{}")
                f.close()

    def  saveTokens(self):
        with open(self.path, "w") as f:
            a = []
            for t in self.tokens:
                temp = { "userid":  t.userid, "timestamp": t.timestamp, "name": t.name}

    def  saveTokens(self):
        a = []
        for t in self.tokens:
            temp = { "userid":  t.userid, "timestamp": t.timestamp, "name": t.name}
            a.append(temp)

        with open(self.path, "w") as f:
            f.write(json.dumps(a))
            f.close()

        self.loadTokens()

    def create(self, userid ,activetime ):
        tk = Token()

        cTime = datetime.datetime.now()
        newTime = cTime + datetime.timedelta(days=30)
        tk.create(userid,  newTime.timestamp())
        
        self.tokens.append(tk.tokenData)

        return tk

    def getTokens(self):
        return self.tokens

    def __contains__(self, tokenid):
        try:
            return self.getTokenById(tokenid).name == tokenid
        except:
            return False





class Token():

    tokenData = None

    def __init__(self, tokenData=None):
        self.tokenData = tokenData

    def create(self, userid, expires):
        """
        userid: str ; ID of the User
        expires: int; time added from current time in seconds
        """
        self.tokenData = TokenData(userid, expires, uuid4().__str__())

    def isActive(self):
        if TokenData == None or self.tokenData.timestamp == None:
            return False
        print(f"{datetime.datetime.now().timestamp()} { self.tokenData.timestamp}")
        if datetime.datetime.now().timestamp() < self.tokenData.timestamp:
            return True
        return False

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

@dataclass(frozen=True, order=True)
class TokenData:
    userid: str
    timestamp: int
    name: str