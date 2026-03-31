import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
from tqdm import tqdm
import json

# Hyperparameters
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.001
DATA_DIR = "dataset"

def get_data_loaders(data_dir, batch_size):
    # Depending on the dataset structure, there might be 'train' and 'test' folders
    # Let's check if 'train' exists inside data_dir
    if os.path.exists(os.path.join(data_dir, "train")):
        train_dir = os.path.join(data_dir, "train")
        test_dir = os.path.join(data_dir, "test")
    else:
        # If it's just a bunch of class folders, we do random split
        train_dir = data_dir
        test_dir = None
        
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    if test_dir is None:
        dataset = datasets.ImageFolder(train_dir, transform=transform)
        train_size = int(0.8 * len(dataset))
        val_size = len(dataset) - train_size
        train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        classes = dataset.classes
    else:
        train_dataset = datasets.ImageFolder(train_dir, transform=transform)
        val_dataset = datasets.ImageFolder(test_dir, transform=transform)
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        classes = train_dataset.classes

    # Save classes map
    with open("classes.json", "w") as f:
        json.dump(classes, f)

    return train_loader, val_loader, classes

def train_model(model, train_loader, val_loader, criterion, optimizer, device, epochs):
    best_acc = 0.0
    
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        running_corrects = 0
        
        print(f"Epoch {epoch+1}/{epochs}")
        for inputs, labels in tqdm(train_loader, desc="Training"):
            inputs = inputs.to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            loss = criterion(outputs, labels)
            
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            
        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_acc = running_corrects.double() / len(train_loader.dataset)
        print(f"Train Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")
        
        # Validation
        model.eval()
        val_loss = 0.0
        val_corrects = 0
        
        with torch.no_grad():
            for inputs, labels in tqdm(val_loader, desc="Validation"):
                inputs = inputs.to(device)
                labels = labels.to(device)
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item() * inputs.size(0)
                val_corrects += torch.sum(preds == labels.data)
                
        val_epoch_loss = val_loss / len(val_loader.dataset)
        val_epoch_acc = val_corrects.double() / len(val_loader.dataset)
        print(f"Val Loss: {val_epoch_loss:.4f} Acc: {val_epoch_acc:.4f}\n")
        
        if val_epoch_acc > best_acc:
            best_acc = val_epoch_acc
            torch.save(model.state_dict(), "gemstone_model.pth")
            print("Saved Best Model!")

def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    train_loader, val_loader, classes = get_data_loaders(DATA_DIR, BATCH_SIZE)
    num_classes = len(classes)
    print(f"Found {num_classes} classes.")
    
    # Using ResNet18
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    train_model(model, train_loader, val_loader, criterion, optimizer, device, EPOCHS)

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        print(f"Data directory '{DATA_DIR}' not found. Please run download_data.py first.")
    else:
        main()
