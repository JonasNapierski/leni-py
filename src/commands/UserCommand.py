
from src.user.UserManager import UserManager
from src.user.User  import User


def command(msg, args):
    
    if args[1] == "create" and len(args) == 4:
            u = User()
            u.create(args[2], u.gen_uuid(), args[3], [])
            u.save_profile()
            
