# -*- coding: utf-8 -*-
"""client-torch.ipynb

Automatically generated by Colaboratory.

Original file is located at:
    https://colab.research.google.com/drive/1POLhDlGHYj1qWCA6SgkLi0jA9gmm8FZt
"""

#pip install flwr

#pip install torch torchvision

from collections import OrderedDict
import torchvision
from torchvision import datasets, models, transforms
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import os
import flwr as fl
import time

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

feature_extract = False 
num_classes = 4
batch_size = 32
data_dir = "/root/Flower-PyTorch-Android-Client/obstacles-sample-20/"
input_size = 224
use_pretrained = True
model_name = 'squeezenet'

def main():
    start_total = time.time()
    # Initialize the model 
    net, input_size = initialize_model(model_name, num_classes, feature_extract, use_pretrained)

    #print(net)
    
    net.to(DEVICE)
    dataloaders_dict = load_data_custom()

    class TLClient(fl.client.NumPyClient):
        def get_parameters(self):
            return [val.cpu().numpy() for _, val in net.state_dict().items()]
            params_dict = zip(net.state_dict().keys(), parameters)
            state_dict = OrderedDict({k: torch.Tensor(v) for k, v in params_dict})
            net.load_state_dict(state_dict, strict=True)
            
        def set_parameters(self, parameters):
            params_dict = zip(net.state_dict().keys(), parameters)
            state_dict = OrderedDict({k: torch.Tensor(v) for k, v in params_dict})
            net.load_state_dict(state_dict, strict=True)

        def fit(self, parameters, config):
            self.set_parameters(parameters)
            train(net, dataloaders_dict, epochs=1)
            return self.get_parameters(), len(dataloaders_dict), {}

        def evaluate(self, parameters, config):
            self.set_parameters(parameters)
            loss, accuracy = test(net, dataloaders_dict)
            #print(float(accuracy))        
            return float(loss), len(dataloaders_dict), {"accuracy":float(accuracy)}
       
    fl.client.start_numpy_client("54.219.134.11:8080", client=TLClient())
    
    end_total = time.time()
    elapsed_total = end_total - start_total
    print("Total training time: " + str(elapsed_total))

def train(net, dataloaders_dict, epochs):
#"""Train the network on the training set."""
    start = time.time()
    params_to_update = net.parameters()
    print("Training Function Start...")
    if feature_extract:
        params_to_update = []
        for name,param in net.named_parameters():
            if param.requires_grad == True:
                params_to_update.append(param)

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(params_to_update, lr=0.001, momentum=0.9)
    net.train()
    for _ in range(epochs):
        for images, labels in dataloaders_dict['train']:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            optimizer.zero_grad()
            loss = criterion(net(images), labels)
            loss.backward()
            optimizer.step()
    end = time.time()
    elapsed = end - start
    print("Training Time Elapsed: " + str(elapsed))
    #print("Training Function End...")

def test(net, dataloaders_dict):
 #   """Validate the network on the entire test set."""
    #print("Test Fucntion Start...")
    criterion = torch.nn.CrossEntropyLoss()
    correct, total, loss, count = 0, 0, 0.0, 0
    net.eval()
    with torch.no_grad():
        for data in dataloaders_dict['val']:
            count = count + 1
            if count == 1:
                break
            #print("Test " + str(count))
            images, labels = data[0].to(DEVICE), data[1].to(DEVICE)
            outputs = net(images)
            loss += criterion(outputs, labels).item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    #accuracy = correct / total
    #print("Test Function End...")
    #return loss, accuracy
    return 0, 0

def load_data_custom():
    data_transforms = {
        'train': transforms.Compose([
            transforms.RandomResizedCrop(input_size),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
        'val': transforms.Compose([
            transforms.Resize(input_size),
            transforms.CenterCrop(input_size),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    print("Initializing Datasets and Dataloaders...")

    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), data_transforms[x]) for x in ['train', 'val']}
# Create training and validation dataloaders
    dataloaders_dict = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=batch_size, shuffle=True, num_workers=4) for x in ['train', 'val']}

    return dataloaders_dict

# Load model and data
def set_parameter_requires_grad(model, feature_extracting):
    if feature_extracting:
        for param in model.parameters():
            param.requires_grad = False
            
def initialize_model(model_name, num_classes, feature_extract, use_pretrained=True):
    # Initialize these variables which will be set in this if statement. Each of these
    #   variables is model specific.
    net = None
    input_size = 0
    
    if model_name == "mobilenet":
        """ MobileNet
        """
        net = models.mobilenet_v2(pretrained=use_pretrained)
        set_parameter_requires_grad(net, feature_extract)
        net.classifier[1] = torch.nn.Linear(in_features=net.classifier[1].in_features, out_features=num_classes)
        net.num_classes = num_classes
        input_size = 224

    elif model_name == "squeezenet":
        """ Squeezenet
        """
        net = models.squeezenet1_0(pretrained=use_pretrained)
        set_parameter_requires_grad(net, feature_extract)
        net.classifier[1] = nn.Conv2d(512, num_classes, kernel_size=(1,1), stride=(1,1))
        net.num_classes = num_classes
        input_size = 224

    else:
        print("Invalid model name, exiting...")
        exit()
    
    print("Model Initialized...")
    
    return net, input_size
    
if __name__ == "__main__":
    main()
