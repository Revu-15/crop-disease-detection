# Setup Instructions

Complete guide to set up the Crop Disease Detection system locally and in the cloud.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Local Development Setup](#local-development-setup)
- [Database Setup](#database-setup)
- [Dataset Preparation](#dataset-preparation)
- [Model Training](#model-training)
- [Running the Application](#running-the-application)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum (16GB recommended for training)
- **GPU**: NVIDIA GPU with CUDA support (optional, for faster training)
- **Disk Space**: 20GB minimum

### Required Software
```bash
# Python 3.8+
python --version

# Git
git --version

# pip (Python package manager)
pip --version
```

## 🚀 Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/Revu-15/crop-disease-detection.git
cd crop-disease-detection
```

### 2. Create Virtual Environment
```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Optional: For GPU support
pip install tensorflow-gpu
```

### 4. Verify Installation
```bash
python -c "import tensorflow; print(tensorflow.__version__)"
python -c "import flask; print(flask.__version__)"
python -c "import torch; print(torch.__version__)"
```

## 🗄️ Database Setup

### SQLite (Development)
```bash
# SQLite is included with Python
# Database will be created automatically on first run

# Initialize database
python -c "from backend.app import create_app; app = create_app(); app.app_context().push()"
```

### PostgreSQL (Production)

#### Installation
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Windows
# Download from https://www.postgresql.org/download/windows/
```

#### Setup Database
```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE crop_disease_detection;

# Create user
CREATE USER crop_user WITH PASSWORD 'your_password';

# Grant privileges
ALTER ROLE crop_user SET client_encoding TO 'utf8';
ALTER ROLE crop_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE crop_user SET default_transaction_deferrable TO on;
ALTER ROLE crop_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE crop_disease_detection TO crop_user;

# Exit psql
\q
```

#### Configure Connection
```bash
# Update .env file
DATABASE_URL=postgresql://crop_user:your_password@localhost/crop_disease_detection
```

## 📊 Dataset Preparation

### Option 1: Download from Kaggle

```bash
# Install Kaggle CLI
pip install kaggle

# Setup credentials
# 1. Go to https://www.kaggle.com/settings/account
# 2. Click "Create New API Token"
# 3. Place kaggle.json in ~/.kaggle/

# Download dataset
kaggle datasets download -d vipoooool/new-plant-diseases-dataset

# Extract
unzip new-plant-diseases-dataset.zip -d ml_model/datasets/
```

### Option 2: Clone from GitHub

```bash
cd ml_model/datasets
git clone https://github.com/spMohanty/PlantVillage-Dataset.git
cd ../..
```

### Option 3: Use Local Images

```bash
# Create directory structure
mkdir -p ml_model/datasets/{train,val}

# Organize images
# ml_model/datasets/
# ├── train/
# │   ├── Tomato_Early_Blight/
# │   ├── Tomato_Late_Blight/
# │   └── ...
# └── val/
#     ├── Tomato_Early_Blight/
#     ├── Tomato_Late_Blight/
#     └── ...
```

### Verify Dataset
```bash
python ml_model/verify_dataset.py --data-dir ml_model/datasets
```

## 🧠 Model Training

### Prepare Configuration
```bash
# Copy config template
cp ml_model/config.example.json ml_model/config.json

# Edit configuration
nano ml_model/config.json
```

### Train Model
```bash
# Train from scratch
python ml_model/train.py \
    --train-dir ml_model/datasets/train \
    --val-dir ml_model/datasets/val \
    --epochs 50 \
    --batch-size 32 \
    --output backend/models/crop_disease_model.h5

# Or with config file
python ml_model/train.py --config ml_model/config.json
```

### Monitor Training
```bash
# Real-time monitoring
tensorboard --logdir ml_model/logs/

# Open in browser: http://localhost:6006
```

### Evaluate Model
```bash
python ml_model/evaluate.py \
    --model backend/models/crop_disease_model.h5 \
    --test-dir ml_model/datasets/val
```

## ▶️ Running the Application

### Backend (Flask API)

```bash
# Development mode
export FLASK_ENV=development
export FLASK_APP=backend/app.py
flask run

# Or with Python
python backend/app.py

# Production mode with Gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 backend:app
```

### Frontend (React)

```bash
cd frontend

# Install dependencies
npm install

# Development server
npm start

# Build for production
npm run build
```

### Access Application

- **API**: http://localhost:5000/api
- **Web App**: http://localhost:3000
- **API Documentation**: http://localhost:5000/api/docs

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_api.py -v

# Run with coverage
python -m pytest tests/ --cov=backend --cov=ml_model

# Run unit tests
python -m unittest discover tests/ -v
```

## 🐛 Troubleshooting

### Common Issues

#### 1. TensorFlow Import Error
```bash
# Solution: Reinstall TensorFlow
pip uninstall tensorflow -y
pip install tensorflow==2.10.0
```

#### 2. CUDA/GPU Issues
```bash
# Verify CUDA installation
nvidia-smi

# Install CUDA-compatible TensorFlow
pip install tensorflow-gpu==2.10.0
```

#### 3. Database Connection Error
```bash
# Check PostgreSQL is running
sudo service postgresql status

# Verify connection string
python -c "from backend.models import db; db.create_all()"
```

#### 4. Dataset Not Found
```bash
# Verify dataset location
ls -la ml_model/datasets/

# Download dataset
python ml_model/download_dataset.py
```

#### 5. Port Already in Use
```bash
# Change port
python backend/app.py --port 5001

# Or kill process using port 5000
lsof -ti:5000 | xargs kill -9
```

### Performance Issues

#### Slow Inference
```bash
# Use GPU
export CUDA_VISIBLE_DEVICES=0

# Optimize model
python ml_model/optimize_model.py --model backend/models/crop_disease_model.h5
```

#### Memory Issues
```bash
# Reduce batch size
python ml_model/train.py --batch-size 16

# Clear cache
python -c "import tensorflow as tf; tf.keras.backend.clear_session()"
```

## 📝 Environment Variables

Create `.env` file:
```bash
# Flask Configuration
FLASK_ENV=development
FLASK_APP=backend/app.py
SECRET_KEY=your_secret_key_here

# Database
DATABASE_URL=sqlite:///crop_disease.db
# Or for PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/crop_disease_detection

# Model Configuration
MODEL_PATH=backend/models/crop_disease_model.h5
MODEL_VERSION=1.0.0

# API Configuration
API_PORT=5000
API_HOST=0.0.0.0
MAX_FILE_SIZE=10485760  # 10MB

# Frontend Configuration
REACT_APP_API_URL=http://localhost:5000/api

# Optional Features
ENABLE_GPU=true
DEBUG_MODE=false
```

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (pip freeze)
- [ ] Database configured and initialized
- [ ] Dataset downloaded and organized
- [ ] Model trained or pre-trained model available
- [ ] Flask backend starts without errors
- [ ] React frontend builds successfully
- [ ] API endpoints respond correctly
- [ ] Tests pass (pytest)

## 🎯 Next Steps

1. Review [API.md](API.md) for API documentation
2. Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment options
3. Read [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
4. Explore example notebooks in `examples/`

---

**Last Updated**: 2026-05-30
