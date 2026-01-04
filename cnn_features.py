import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from pathlib import Path

# =========================
# LOAD PRETRAINED CNN
# =========================
model = models.resnet18(pretrained=True)
model = torch.nn.Sequential(*list(model.children())[:-1])
model.eval()

# =========================
# TRANSFORM
# =========================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# =========================
# FEATURE EXTRACTOR
# =========================
def extract_cnn_features(image_path):
    image = Image.open(image_path).convert("RGB")
    tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        features = model(tensor)

    # Flatten to 1D vector
    features = features.view(-1).numpy()

    # 🔥 Keep only first 20 features (stable & fast)
    return features[:20]