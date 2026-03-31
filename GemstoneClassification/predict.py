import sys
import json
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image

def predict_image(image_path, model_path="gemstone_model.pth", classes_path="classes.json"):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    try:
        with open(classes_path, "r") as f:
            classes = json.load(f)
    except FileNotFoundError:
        print(f"Error: {classes_path} not found. Please train the model first.")
        return
        
    num_classes = len(classes)
    
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
    
    try:
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        print(f"Error loading image '{image_path}': {e}")
        return
        
    image_tensor = transform(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        outputs = model(image_tensor)
        _, preds = torch.max(outputs, 1)
        
    predicted_class = classes[preds[0].item()]
    print(f"Predicted Gemstone: {predicted_class}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python predict.py <path_to_image>")
    else:
        predict_image(sys.argv[1])
