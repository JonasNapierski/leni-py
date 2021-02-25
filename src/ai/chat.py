import random
import json
import torch
from .AI import NeuralNet
from nltk_utils import bag_of_words, tokenize

class Chat():
    def __init__(self) -> None:
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        with open('intents.json', "r") as f:
            intents = json.load(f)

        FILE = "data.pth"
        data = torch.load(FILE)

        input_size = data['input_size']
        hidden_size = data['hidden_size']
        output_size = data['output_size']
        all_words = data['all_words']
        tags = data['tags']
        model_state = data['model_state']

        model = NeuralNet(input_size, hidden_size, output_size).to(device)
        model.load_state_dict(model_state)
        model.eval()

        bot_name = "Leni"
        print("Let's chat! type 'quit' to exit")
        while True:
            sentence = input("You: ")
            if sentence == "quit":
                break
            tokenized = tokenize(sentence)
            bog = bag_of_words(tokenized, all_words)
            bog = bog.reshape(1, bog.shape[0])
            bog = torch.from_numpy(bog)

            output = model(bog)
            _, predicted = torch.max(output, dim=1)
            tag = tags[predicted.item()]

            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]
            
            if prob.item() > 0.75:
                for intent in intents["intents"]:
                    if tag == intent["tag"]:
                        print(f"{bot_name}: {random.choice(intent['patterns'])}")
            else:
                print(f"{bot_name}: I do not understand...")