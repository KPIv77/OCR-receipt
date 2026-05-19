import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image


class ReceiptClassifier:
    
    # Initialize the classifier 
    def __init__(
        self, 
        model_path: str,
        class_names: list[str],
        img_size: int,
        device: torch.device,
    ):
        self.class_names = class_names
        self.device = device
        
        # Define the image transformations
        self.transform = transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
        ])
        
        # Load the model and set it to evaluation mode
        self.model = self._load_model(model_path, len(class_names))

    def _load_model(self, model_path: str, num_classes: int) -> nn.Module:
        
        model = models.mobilenet_v2(weights=None)
        
        num_features = model.classifier[1].in_features
        
        model.classifier = nn.Sequential(
            nn.Dropout(0.3),                          
            nn.Linear(num_features, num_classes)      
        )
        
        model.load_state_dict(
            torch.load(model_path, map_location=self.device)
        )
        
        model = model.to(self.device)
        model.eval()  
        return model
    
    def predict(self, image_path: str) -> dict:

        image = Image.open(image_path).convert("RGB")
        image = self.transform(image)
        image = image.unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(image)                         
            probs = torch.softmax(outputs, dim=1)               
            confidence, predicted = torch.max(probs, 1)         
        return {
            "bank": self.class_names[predicted.item()],
            "confidence": round(float(confidence.item()), 4)    
        }