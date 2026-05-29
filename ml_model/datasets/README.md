# Dataset Sources

This directory is for training and validation datasets.

## Recommended Datasets

### PlantVillage Dataset
- **Source:** https://github.com/spMohanty/PlantVillage-Dataset
- **Size:** ~50,000 images
- **Crops:** Tomato, Potato, Corn, and many others
- **Diseases:** Multiple disease and healthy leaf images

### Directory Structure
```
datasets/
├── train/
│   ├── Tomato_Early_Blight/
│   ├── Tomato_Late_Blight/
│   ├── Potato_Early_Blight/
│   └── ...
└── val/
    ├── Tomato_Early_Blight/
    ├── Tomato_Late_Blight/
    ├── Potato_Early_Blight/
    └── ...
```

## Download Instructions

### Option 1: Download from Kaggle
```bash
# Install kaggle CLI
pip install kaggle

# Download PlantVillage dataset
kaggle datasets download -d vipoooool/new-plant-diseases-dataset
unzip new-plant-diseases-dataset.zip
```

### Option 2: Clone from GitHub
```bash
cd datasets
git clone https://github.com/spMohanty/PlantVillage-Dataset.git
```

## Data Preparation

1. Download dataset
2. Organize into train/val folders
3. Use 80% for training, 20% for validation
4. Ensure balanced class distribution

## Training

```bash
cd ..
python ml_model/train.py \
    --train-dir datasets/train \
    --val-dir datasets/val \
    --epochs 50 \
    --batch-size 32 \
    --output backend/models/crop_disease_model.h5
```

## Data Statistics

| Dataset | Type | Size |
|---------|------|------|
| PlantVillage | RGB Images | ~50K |
| Image Size | Standard | 256x256 - 512x512 |
| Classes | Disease Types | 38 classes |
| Training/Val Split | Ratio | 80/20 |

## Important Notes

- All images should be in RGB format (JPG, PNG)
- Minimum image size: 128x128 pixels
- Maximum image size: 2048x2048 pixels
- Recommended: 224x224 for the model
- Ensure class directories contain only image files
