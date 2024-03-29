from src.ai.AI import Training
from src.Debugger import Debug

class AICommand():
    def __init__(self, bot, moduleManager):
        self.bot = bot
        self.moduleManager = moduleManager


    def command(self, msg, args):
        if len(args) > 1:
            if args[1] == "print":
                self.bot.print()

            elif args[1] == "train" and len(args) == 3:
                for module in self.moduleManager.modules:
                    tmp_arr = []
                    tmp_config = module.getConfig()

                    for i in range(len(tmp_config["commands"])):
                        if tmp_config["commands"][i]["language"] == args[2]:
                            tmp_arr.extend(tmp_config["commands"][i]["examples"])
                    
                    self.bot.add(tmp_arr, module.module_name)
                self.bot.create_set()
                self.bot.train(num_epochs=5000, batch_size=8, learning_rate=0.01, hidden_size=8, num_workers=0, FILE_PATH="./data/ai/Module_Namer.ai")
            
            elif args[1] == "reload":
                self.bot.load(FILE_PATH="./data/ai/Module_Namer.ai")
                Debug.print("AI-CMD: reloaded")

            elif args[1] == "save" and len(args) > 2:
                
                try:
                    self.bot.save(self.bot.data, args[2])
                    Debug.print(f"AI-CMD: AI saved to {args[2]}")
                except Exception as exp:
                    Debug.print(exp)
                    Debug.print("AI-CMD: Saving file failed!")
        else:
            Debug.print("AI-CMD: AI print | Print the current Dataset")
            Debug.print("AI-CMD: AI train [language] | trains the  AI on the language")