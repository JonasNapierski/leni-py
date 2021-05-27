
from src.user.UserManager import UserManager
from src.user.User  import User
import hashlib

def command(msg, args):
    
    if args[1] == "create" and len(args) == 4:
            u = User()
            u.create(args[2], u.gen_uuid(), str(hashlib.md5(str(args[3]).encode()).hexdigest()), [])
            u.save_profile()
            
