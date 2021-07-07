from src.ai.AI import Training
from src.Debugger import Debug

class AICommand():
    def __init__(self, bot, moduleManager):
        self.bot = bot
        self.moduleManager = moduleManager


    def command(self, msg, args):
        if args[1] == "print":
            self.bot.print()

        elif args[1] == "train" and len(args) == 3:
            for mm in self.moduleManager.modules:
                mcfg = mm.getConfig()
                self.bot.add(mcfg[str(args[2]).upper()], mm.module_name)

            self.bot.create_set()
            self.bot.train(num_epochs=5000, batch_size=8, learning_rate=0.01, hidden_size=8, num_workers=0, FILE_PATH="DATA.pth")
        
        elif args[1] == "reload":
            self.bot.load(FILE_PATH="DATA.pth")
            Debug.print("AI reloaded")
        else:
            Debug.print("AI print | Print the current Dataset")
            Debug.print("AI train [language] | trains the  AI on the language")