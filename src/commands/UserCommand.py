
from src.user.UserManager import UserManager
from src.user.User  import User
from src.Debugger import Debug
import hashlib

class UserCommand():
    userManager = None

    def __init__(self, usermanager):
        self.userManager = usermanager

    def command(self, msg, args):
        
        if args[1] == "create" and len(args) == 4:
                u = User()
                u.create(args[2], u.gen_uuid(), str(hashlib.md5(str(args[3]).encode()).hexdigest()), [])
                u.save_profile()
                self.userManager.load_users()
        if args[1] == "list":
            i = 1
            for u in self.userManager.get_users():
                Debug.print(f"{i}: {u.displayname} / {u.uuid}")
                i = i+1
