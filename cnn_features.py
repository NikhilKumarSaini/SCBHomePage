import torch
import torchvision.transforms as T
from torchvision import models
from PIL import Image
import numpy as np

# Pretrained ResNet18
_model = models.resnet18(pretrained=True)
_model.fc = torch.nn.Identity()
_model.eval()

_transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor()
])

def extract_cnn_features(image_path: str) -> list:
    img = Image.open(image_path).convert("RGB")
    x = _transform(img).unsqueeze(0)

    with torch.no_grad():
        feats = _model(x).numpy().flatten()

    return feats.tolist()