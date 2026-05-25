# Smart Crop Disease Detection System

An AI-powered web application that detects crop diseases from leaf images using machine learning and provides treatment recommendations.

## 🌿 Features

✅ **Disease Detection** - Upload leaf images and get AI-powered disease identification
✅ **Disease Information** - Detailed info about symptoms, prevention, and treatment
✅ **Treatment Recommendations** - Specific pesticide and fertilizer suggestions
✅ **Upload History** - Track all previous uploads and results
✅ **Responsive Design** - Works on desktop, tablet, and mobile devices
✅ **Farmer-Friendly Interface** - Simple and intuitive UI for non-tech users

## 🎯 Supported Crops & Diseases

### Tomato
- Early Blight
- Late Blight
- Leaf Spot
- Septoria Leaf Spot
- Yellow Leaf Curl

### Potato
- Early Blight
- Late Blight

### Corn
- Common Rust
- Gray Leaf Spot

## 🛠️ Tech Stack

**Frontend:**
- HTML5
- CSS3
- JavaScript (Vanilla)
- Responsive Design

**Backend:**
- Python 3.8+
- Flask 2.3.3
- Flask-CORS
- Flask-SQLAlchemy

**Machine Learning:**
- TensorFlow/Keras
- OpenCV
- Pillow
- NumPy
- Scikit-learn

**Database:**
- SQLite3

## 📦 Project Structure

```
crop-disease-detection/
├── frontend/                 # Frontend files
│   ├── index.html           # Home page
│   ├── upload.html          # Image upload page
│   ├── result.html          # Results page
│   ├── history.html         # History page
│   ├── css/
│   │   ├── style.css        # Main styles
│   │   └── responsive.css   # Mobile responsive
│   └── js/
│       ├── app.js           # App logic
│       ├── upload.js        # Upload handler
│       ├── api.js           # API calls
│       └── utils.js         # Utilities
├── backend/
│   ├── app.py               # Flask app entry
│   ├── config.py            # Configuration
│   ├── requirements.txt     # Python dependencies
│   ├── api/
│   │   ├── routes.py        # API endpoints
│   │   └── disease_detector.py  # ML logic
│   ├── database/
│   │   └── models.py        # Database models
│   ├── data/
│   │   └── disease_database.json  # Disease info
│   └── uploads/             # Uploaded images
├── static/                  # Static files
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Revu-15/crop-disease-detection.git
cd crop-disease-detection
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r backend/requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env file with your configuration
```

5. **Initialize database**
```bash
cd backend
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
```

6. **Run the application**
```bash
python backend/app.py
```

The application will be available at `http://localhost:5000`

## 📖 API Documentation

See [API.md](docs/API.md) for detailed API endpoints documentation.

### Main Endpoints

```
GET  /                    - Home page
GET  /upload              - Upload page
GET  /result              - Results page
GET  /history             - History page

GET  /api/health          - Health check
POST /api/predict         - Predict disease
GET  /api/history         - Get upload history
GET  /api/diseases        - Get all diseases
GET  /api/disease/<name>  - Get disease details
```

## 🧠 Machine Learning Model

The system uses a pre-trained CNN model for disease detection. To use your own model:

1. Train your model using `ml_model/train.py`
2. Save the model as `.h5` format
3. Place it in `backend/models/crop_disease_model.h5`
4. Update class names in `api/disease_detector.py`

## 📚 Documentation

- [Setup Guide](docs/SETUP.md) - Detailed setup instructions
- [API Documentation](docs/API.md) - API endpoints reference
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment
- [Contributing](docs/CONTRIBUTING.md) - Contribution guidelines

## 🐛 Troubleshooting

### Port already in use
```bash
# Change port in backend/app.py
app.run(port=5001)
```

### Database errors
```bash
# Reset database
rm backend/database/crop_diseases.db
python backend/app.py  # Will recreate database
```

### Model not loading
- Ensure model file exists in `backend/models/crop_disease_model.h5`
- Check file path in `backend/config.py`
- Model will use mock predictions if file not found

## 📱 Usage

1. **Home Page** - Introduction and features overview
2. **Upload Page** - Drag & drop or select a crop leaf image
3. **Results Page** - View disease detection results and recommendations
4. **History Page** - View previous uploads and results

## 🔒 Security

- Input validation on file uploads
- File size limits (16MB max)
- Allowed file types (JPG, PNG, GIF)
- CORS enabled for specified origins
- SQL injection protection via SQLAlchemy ORM

## 📊 Performance

- Average prediction time: 2-5 seconds
- Supports concurrent requests
- Optimized image preprocessing
- Efficient database queries

## 🌐 Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for:
- Heroku deployment
- AWS deployment
- Docker containerization
- Production best practices

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Authors

- **POLAMREDDY REVANTH REDDY** - Initial development

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 📧 Support

For issues and questions, please open an issue on GitHub.

## 🎓 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [TensorFlow/Keras Guide](https://www.tensorflow.org/guide)
- [Web Development Basics](https://developer.mozilla.org/en-US/docs/Web)

## 🚀 Future Enhancements

- [ ] Real-time camera feed processing
- [ ] Mobile app (React Native)
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] User authentication system
- [ ] Export reports (PDF/CSV)
- [ ] Integration with weather APIs
- [ ] IoT sensor integration

---

**Last Updated:** May 2026  
**Status:** Active Development  
**Version:** 1.0.0
