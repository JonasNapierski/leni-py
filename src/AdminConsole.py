from threading import Thread
import sys
import os
from src.Debugger import Debug

class AdminConsole():
    isRunning = False

    def __init__(self):
        pass

    def run(self):
        Debug.print("run AdminConsole thread")
        self.isRunning = True


    def input_loop(self):
        if self.isRunning == False:
            return
        
        while self.isRunning:
            sys.stdin = open(0)
            c = sys.stdin.readline().strip("\n\r")


            if c == "exit":
                self.isRunning = False
                Debug.print("Admin-Console closed!")
            Debug.print(c)