import numpy as np
import logging
import os
import torch
import torch.nn as nn
from src.core.ai.nltk_utils import NLTKUtils
from src.core.settings.logging import LOGGING_NAME_CORE
from torch.utils.data import Dataset, DataLoader

nu = NLTKUtils()
log = logging.getLogger(LOGGING_NAME_CORE)

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)

        # no activation and no softmax
        return out


class Training():
    def __init__(self, name: str):
        self.name = name
        selected_dev = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.device = torch.device(selected_dev)
        log.debug(f"Training on: {self.device}")

        self.data = {}
        self.all_words = []
        self.tags = []
        self.xy = []
        self.x_train = []
        self.y_train = []
        self.name = ""

    def add(self, pattern_sentence, tag):
        self.tags.append(tag)
        for sentence in pattern_sentence:
            w = nu.tokenize(sentence)  # add the sentece to all words
            self.all_words.extend(w)

            self.xy.append((w, tag))

    def filter(self, ignore_list=[]):
        all_words = self.all_words
        clean_list = [nu.stem(w) for w in all_words if w not in ignore_list]
        # remove duplicates and sorts
        clean_list = sorted(set(clean_list))
        self.all_words = clean_list
        self.tags = sorted(set(self.tags))

    def print(self):
        print(len(self.xy), "Patterns")
        print(len(self.tags), "tags:", self.tags)
        print(len(self.all_words), "unique stemmed words:", self.all_words)

    def create_set(self):
        x_train = []
        y_train = []

        for (pattern_sentence, tag) in self.xy:
            bag = nu.bag_of_words(pattern_sentence, self.all_words)
            x_train.append(bag)

            label = self.tags.index(tag)
            y_train.append(label)

        x_train = np.array(x_train)
        y_train = np.array(y_train)

        self.x_train = x_train
        self.y_train = y_train

    def train(self,
              num_epochs,
              batch_size,
              learning_rate,
              hidden_size,
              num_workers,
              FILE_PATH):
        input_size = len(self.x_train[0])
        output_size = len(self.tags)

        dataset = ChatDataset(self.x_train, self.y_train)
        train_loader = DataLoader(
                dataset=dataset,
                batch_size=batch_size,
                shuffle=True,
                num_workers=num_workers)

        model = NeuralNet(
                input_size,
                hidden_size,
                output_size).to(device=self.device)

        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

        for epoch in range(num_epochs):
            for (words, labels) in train_loader:
                words = words.to(self.device)
                labels = labels.to(dtype=torch.long).to(self.device)

                outpus = model(words)

                loss = criterion(outpus, labels)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                if (epoch+1) % 100 == 0:
                    log.debug(f"{self.name} | Epoch [{epoch+1}/{num_epochs}]\
                            , Loss: {loss.item():.9f}")
        log.debug(f"{self.name} | Final loss: {loss.item():.5f}")

        self.data = {
            'model_state': model.state_dict(),
            'input_size': input_size,
            "output_size": output_size,
            "hidden_size": hidden_size,
            "all_words": self.all_words,
            "tags": self.tags
        }

        
        if not os.path.exists("./data/ai"):
            os.makedirs("./data/ai")
        torch.save(self.data, FILE_PATH)
        return self.data

    def save(self,data,  FILE_PATH=""):
        try:
            if not os.path.exists("./data/ai"):
                os.makedirs("./data/ai")
            torch.save(data, FILE_PATH)
            return True
        except:
            return False
    def load(self, FILE_PATH):
        try:
            self.data = torch.load(FILE_PATH)

            input_size = self.data['input_size']
            hidden_size = self.data['hidden_size']
            output_size = self.data['output_size']
            self.all_words = self.data['all_words']
            self.tags = self.data['tags']
            model_state = self.data['model_state']

            self.model = NeuralNet(input_size, hidden_size, output_size).to(self.device)
            self.model.load_state_dict(model_state)
            self.model.eval()
            return True
        except:
            log.debug(f"AI File loading Failed: {FILE_PATH}")
            return False
        

    def process(self, msg: str):
        '''
            argument: msg [string]

            return (module-name [string]; probability [float])
        '''

        test = str()
        tokenized = nu.tokenize(msg)
        bog = nu.bag_of_words(tokenized, self.all_words)
        bog = bog.reshape(1, bog.shape[0])
        bog = torch.from_numpy(bog)

        output = self.model(bog)
        _, predicted = torch.max(output, dim=1)
        tag = self.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        return (self.tags[predicted.item()], prob.item())

class ChatDataset(Dataset):
    def __init__(self, X_train, y_train):

        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # we can call len(dataset) to return the size
    def __len__(self):
        return self.n_samples
