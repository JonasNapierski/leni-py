from src.user.User import User
import os 
from glob import glob
import json

class UserManager():
    users=[]
    path=""


    def __init__(self, path):
        if not os.path.exists(f"{path}/users"):
            os.makedirs(f"{path}/users")
            
        self.path = path


        self.load_users()
               
    def load_users(self):
        self.users = []
        files = glob(f"{self.path}/users/*")

        for f in files:
           
            u = User(self.path)
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
    
    def get_user_by_name(self, username):
        for user in self.users:
            if user.username == username:
                return user

        return None 