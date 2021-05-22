from src.user.User import User
import os 
from glob import glob
import json

class UserManager():
    users=[]
    path=""


    def __init__(self, path):
        if not os.path.exists(path):
            return
        self.path = path

        print("user data base found!")
        files = glob(f"{path}/users/*")

        for f in files:
           
            u = User(path)
            u.load(f)
            self.users.append(u)       


    def get_users(self):
        return self.users
        
    def user_exists(self, uuid):
        if self.get_user(uuid) == None:
            return False

        return True 

    def get_user_by_token(self, token):
        for u in self.users:
            if u.check_for_token(token):
                return u

    def add_token(self, uuid, token):
        for user in self.users:
            if user.check_uuid(uuid):
                user.add_token(token)

    def get_user(self, uuid):
        for user in self.users:
            if user.check_uuid(uuid):
                return user
        return None 
    
    def get_user_by_name(self, displayname):
        for user in self.users:
            if user.displayname == displayname:
                return user

        return None 