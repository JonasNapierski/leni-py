import logging
import hashlib
from src.user.UserManager import UserManager
from src.user.User  import User
from src.core.settings.logging import LOGGING_NAME_CORE

log = logging.getLogger(LOGGING_NAME_CORE)

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
                log.debug(f"{i}: {u.username} / {u.uuid}")
                i = i+1
