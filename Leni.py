import os 
from src.Module import Module
from src.ModuleController import ModuleController

from  src.ai.AI import Training


bot = Training()
bot.add(["hi", "hello", "welcome", "tach", "guten morgen", "guten tag"] ,"morning")
bot.add(["cia", "tschüss", "bye", "bis bald"],"goodbye")
bot.filter([".","!","?"])

bot.create_set()
bot.train(num_epochs=5000, batch_size=8, learning_rate=0.001, hidden_size=8, num_workers=0, FILE_PATH="DATA.pth")
bot.load(FILE_PATH="DATA.pth")
bot.print()
while True:
    print(bot.process(input(">")))

mc = ModuleController("./modules")
mc.find_all_files()
mc.load_all_module()
for m in mc.modules:
    m.exec("")