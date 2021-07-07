from threading import Thread
import sys
import importlib
import os
from src.commands.AICommand import AICommand
from src.commands.UserCommand import UserCommand
from src.Debugger import Debug
from src.tokens.TokenManager import TokenManager
from src.user.UserManager import UserManager






class AdminConsole():
    isRunning = False
    userManager = None 
    tokenManager = None
    moduleManager = None

    register_commands = {}

    def init_commands(self):
        uc = UserCommand(self.userManager)

        ai_cmd = AICommand(self.bot, self.moduleManager)

        self.register_commands = {
            "user": uc,
            "ai": ai_cmd
        }

    def __init__(self, userManager, tokenManager, bot, moduleManager):
        self.userManager = userManager
        self.tokenManager = tokenManager
        self.moduleManager = moduleManager
        self.bot = bot
        
        self.init_commands()

    def run(self):
        Debug.print("run AdminConsole thread")
        self.isRunning = True


    def input_loop(self):
        if self.isRunning == False:
            return
        
        while self.isRunning:
            sys.stdin = open(0)
            c = sys.stdin.readline().strip()


            if c == "exit":
                self.isRunning = False
                Debug.print("Admin-Console closed!")

            args = c.split()
            
            for cmd in self.register_commands:
                if args[0] == cmd:
                    #importlib.reload(self.register_commands[cmd])
                    try:
                        self.register_commands[cmd].command(c, args)
                    except:
                        Debug.print(f"{cmd} failed!")