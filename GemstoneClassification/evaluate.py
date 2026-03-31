import os
import json
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from tqdm import tqdm
from sklearn.metrics import classification_report, accuracy_score

def evaluate_model(test_dir="dataset/test", model_path="gemstone_model.pth", classes_path="classes.json"):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    try:
        with open(classes_path, "r") as f:
            classes = json.load(f)
    except FileNotFoundError:
        print(f"Error: {classes_path} not found. Please train the model first.")
        return
        
    num_classes = len(classes)
    
    # Load model
    model = models.resnet18(weights=None)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)
    
    try:
        model.load_state_dict(torch.load(model_path, map_location=device))
    except FileNotFoundError:
        print(f"Error: {model_path} not found. Please train the model first.")
        return
        
    model = model.to(device)
    model.eval()
    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    
    print(f"Loading test dataset from {test_dir}...")
    try:
        test_dataset = datasets.ImageFolder(test_dir, transform=transform)
        test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
    except Exception as e:
        print(f"Failed to load test dataset: {e}")
        return

    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for inputs, labels in tqdm(test_loader, desc="Evaluating"):
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            
    acc = accuracy_score(all_labels, all_preds)
    print(f"\nOverall Test Accuracy: {acc * 100:.2f}%\n")
    
    print("Classification Report:")
    # Using zero_division=0 to prevent warnings
    print(classification_report(all_labels, all_preds, target_names=classes, zero_division=0))

if __name__ == "__main__":
    evaluate_model()
