# Crop Disease Detection Documentation

Welcome to the comprehensive documentation for the Crop Disease Detection system. This project uses deep learning to identify crop diseases from images and provide treatment recommendations.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Documentation Files](#documentation-files)
- [Support](#support)

## 🚀 Quick Start

1. **Setup Environment**
   ```bash
   git clone https://github.com/Revu-15/crop-disease-detection.git
   cd crop-disease-detection
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Download Datasets**
   - See [SETUP.md](SETUP.md) for detailed dataset download instructions

3. **Run the Application**
   ```bash
   python backend/app.py
   ```

4. **Access API**
   - API: http://localhost:5000/api
   - Documentation: See [API.md](API.md)

## 📊 Project Overview

This crop disease detection system leverages:
- **Deep Learning**: Convolutional Neural Networks (CNN) for image classification
- **TensorFlow/Keras**: Model training and inference
- **Flask**: RESTful API backend
- **React**: Web frontend
- **Mobile Support**: Cross-platform mobile applications

### Supported Crops
- Tomato
- Potato
- Corn
- Grape
- Apple
- Strawberry
- Pepper Bell
- And more...

### Disease Detection
The model can identify:
- Early Blight
- Late Blight
- Leaf Spot
- Powdery Mildew
- Healthy leaves
- And 30+ other diseases

## ✨ Features

### Core Features
- 🎯 **Accurate Detection**: 95%+ accuracy on PlantVillage dataset
- 📱 **Mobile Friendly**: Responsive web interface
- 🔍 **Real-time Analysis**: Instant disease detection
- 💡 **Smart Recommendations**: Treatment and prevention tips
- 📊 **Batch Processing**: Analyze multiple images
- 📈 **Performance Metrics**: Detailed accuracy reports

### Advanced Features
- User authentication and profiles
- Disease history tracking
- Confidence scoring
- Similar disease suggestions
- Disease severity assessment
- Treatment effectiveness tracking

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│              Web & Mobile Applications                   │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                   Flask API Backend                      │
│            RESTful API Endpoints & Auth                  │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              Disease Detection Engine                    │
│          (TensorFlow/Keras CNN Model)                    │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│           Database & File Storage                        │
│         (PostgreSQL, SQLite, Cloud Storage)              │
└─────────────────────────────────────────────────────────┘
```

## 📚 Documentation Files

### [SETUP.md](SETUP.md)
Complete setup and installation instructions including:
- Environment setup
- Dependency installation
- Database configuration
- Dataset download and preparation
- Model training
- Testing setup

### [API.md](API.md)
API reference documentation covering:
- Authentication
- Disease endpoints
- Prediction endpoints
- User management
- Request/response formats
- Error handling
- Rate limiting

### [DEPLOYMENT.md](DEPLOYMENT.md)
Deployment guides for:
- Local development
- Docker deployment
- Kubernetes setup
- Cloud platforms (AWS, GCP, Azure)
- CI/CD pipelines
- Monitoring and logging

### [CONTRIBUTING.md](CONTRIBUTING.md)
Guidelines for:
- Code contribution
- Pull request process
- Coding standards
- Testing requirements
- Documentation standards
- Issue reporting

## 🔧 Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | Python, Flask |
| **ML/AI** | TensorFlow, Keras, scikit-learn |
| **Frontend** | React, TypeScript |
| **Database** | PostgreSQL, SQLite |
| **Deployment** | Docker, Kubernetes |
| **Cloud** | AWS, Google Cloud, Azure |
| **Testing** | pytest, unittest, Jest |

## 📦 Project Structure

```
crop-disease-detection/
├── backend/              # Flask API and business logic
├── frontend/             # React web application
├── ml_model/            # Machine learning models and training
├── mobile/              # Mobile app (React Native/Flutter)
├── tests/               # Test suites
├── docs/                # Documentation
├── docker/              # Docker configuration
└── requirements.txt     # Python dependencies
```

## 🎓 Getting Started Guides

### For Users
1. Read [SETUP.md](SETUP.md) for installation
2. Check [API.md](API.md) for available endpoints
3. Review example requests in API documentation

### For Developers
1. Follow [CONTRIBUTING.md](CONTRIBUTING.md)
2. Set up development environment from [SETUP.md](SETUP.md)
3. Review code structure in README
4. Run tests before submitting PRs

### For Deployment
1. Review [DEPLOYMENT.md](DEPLOYMENT.md)
2. Choose deployment platform
3. Follow platform-specific instructions
4. Set up monitoring and logging

## 📊 Performance Metrics

- **Model Accuracy**: 95.2% on test dataset
- **Inference Time**: ~100ms per image
- **Supported Resolutions**: 128x128 to 2048x2048
- **Batch Processing**: Up to 100 images/second
- **API Response Time**: <500ms average

## 🤝 Support

### Documentation
- 📖 See respective documentation files
- 💬 GitHub Discussions for Q&A
- 📝 Issue tracker for bug reports

### Community
- GitHub Issues: Report bugs and suggest features
- Pull Requests: Contribute code improvements
- Discussions: Ask questions and share ideas

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- PlantVillage dataset for training data
- TensorFlow and Keras communities
- Contributors and testers

---

**Last Updated**: 2026-05-30
**Version**: 1.0.0
