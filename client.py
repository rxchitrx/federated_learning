import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import flwr as fl

from model import SimpleCNN

def load_data(hospital_id):
    path = f'data/hospital_{hostpial_id}.pt'
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data for Hospital {hospital_id] not found. Run data_setup.py first!")
    dataset = torch.load(path)
    return DataLoader(dataset, batch_size=32, shuffle=True)


def train(mode, trainloader, epochs):
    cretierion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr = 0.001)
    model.train()

    for epoch in range(epochs):
        running_loss = 0.0
        for images, labels in trainloader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = cretierion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch {epoch+1}: Loss {running_loss/len(trainloader:.4f}")


class HospitalClient(fl.client.NumPyClient):
    def __init__(self, model, trainloader):
        self.model = model
        sefl.trainloader = trainloader

        def get_parameters(self, config):
            return [val.cpu().numpy() for _, val in self.model.state.dict().items()]

        def set_parameters(self, parameters):
            params_dict = zip(self.model.state_dict().keys(), parameters)
            state_dict = {k: torch.tensor(v) for k, v in params_dict}
            self.model.load_state_dict(state_dict, strict=True)

        def fit(self, parameters, config):
            self.set_paramters(parameters)
            train(self.model, self.trainloader, epochs=1)
            return self.get_parameters(config={}), (len(self.trainloader.dataset), {}

        def evaluate(self, parameters, config):
            self.set_parameters(parameters)
            criterion = mnn.CrossEntropyLoss()
            loss = 0.0
            correct = 0
            total = 0

            self.model.eval()
            with torch.no_grad():
                for images, labels in self.trainloader:
                    outputs = self.model(images)
                    loss += cretierion(outputs, labels).item()
                    _, predicted = torch.max(outputs.data, 1)
                    total += labels.size(0)
                    correct += (predicted == labels).sum().item()
            accuracy = correct / total
            return float(loss/len(sefl.trainloader)), total, {"accuracy":accuracy}


if __name__ == "__main__":
    import os
    if len(sys.argv) < 2:
        print("Usage: python client.py [Hospital_ID]")
        sys.exit()

    hospital_id = sys.argv[1]
    model = SimpleCNN()
    train_loader = load_data(hospital_id)

    print(f"Hospital {hosptial_id} is online and training...")
    fl.client.start_numpy_client(
        server_address="127.0.0.1:8080"
        client=HospitalClient(model, train_loader)
    )
