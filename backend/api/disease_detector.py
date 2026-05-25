import os
import json
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image
import cv2

class DiseaseDetector:
    """Disease detection using ML model"""
    
    def __init__(self, app):
        """Initialize disease detector"""
        self.app = app
        self.model = None
        self.class_names = None
        self.disease_db = None
        self.load_model()
        self.load_disease_database()
    
    def load_model(self):
        """Load pre-trained ML model"""
        try:
            model_path = self.app.config['MODEL_PATH']
            if os.path.exists(model_path):
                self.model = load_model(model_path)
                # Define class names based on training data
                self.class_names = [
                    'Tomato Early Blight',
                    'Tomato Late Blight',
                    'Tomato Leaf Spot',
                    'Tomato Septoria Leaf Spot',
                    'Tomato Yellow Leaf Curl',
                    'Potato Early Blight',
                    'Potato Late Blight',
                    'Corn Common Rust',
                    'Corn Gray Leaf Spot',
                    'Healthy Leaf'
                ]
                print("✓ ML Model loaded successfully")
            else:
                print("⚠ Model file not found. Using mock predictions.")
                self.class_names = [
                    'Tomato Early Blight',
                    'Tomato Late Blight',
                    'Tomato Leaf Spot',
                    'Potato Early Blight',
                    'Potato Late Blight',
                    'Corn Common Rust',
                    'Healthy Leaf'
                ]
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
    
    def load_disease_database(self):
        """Load disease information from JSON"""
        try:
            db_path = self.app.config['DISEASE_DB_PATH']
            if os.path.exists(db_path):
                with open(db_path, 'r') as f:
                    self.disease_db = json.load(f)
                print("✓ Disease database loaded successfully")
            else:
                self.disease_db = self._get_default_disease_db()
                print("⚠ Using default disease database")
        except Exception as e:
            print(f"Error loading disease database: {e}")
            self.disease_db = self._get_default_disease_db()
    
    def preprocess_image(self, image_path, target_size=(224, 224)):
        """Preprocess image for model prediction"""
        try:
            img = Image.open(image_path).convert('RGB')
            img = img.resize(target_size)
            img_array = keras_image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0  # Normalize
            return img_array
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            raise
    
    def predict(self, image_path):
        """Predict disease from image"""
        try:
            # Preprocess image
            img_array = self.preprocess_image(image_path)
            
            # Make prediction
            if self.model:
                predictions = self.model.predict(img_array)
                confidence = float(np.max(predictions))
                class_idx = int(np.argmax(predictions))
            else:
                # Mock prediction for testing
                confidence = np.random.uniform(0.7, 0.99)
                class_idx = np.random.randint(0, len(self.class_names))
            
            disease_name = self.class_names[class_idx]
            
            # Get disease details
            disease_info = self.get_disease_info(disease_name)
            
            return {
                'success': True,
                'disease_name': disease_name,
                'confidence': round(confidence, 4),
                'class_idx': class_idx,
                'disease_info': disease_info
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_disease_info(self, disease_name):
        """Get disease information from database"""
        if disease_name in self.disease_db:
            return self.disease_db[disease_name]
        else:
            return self.disease_db.get('Unknown Disease', {})
    
    def _get_default_disease_db(self):
        """Return default disease database"""
        return {
            'Tomato Early Blight': {
                'crop_type': 'Tomato',
                'description': 'A fungal disease affecting tomato leaves',
                'symptoms': 'Brown spots with concentric rings on lower leaves',
                'prevention_tips': 'Remove infected leaves, improve air circulation, avoid overhead watering',
                'suggested_pesticide': 'Chlorothalonil or Mancozeb',
                'treatment_duration': '7-14 days',
                'severity': 'Medium',
                'recommended_fertilizer': 'Potassium-rich fertilizer'
            },
            'Tomato Late Blight': {
                'crop_type': 'Tomato',
                'description': 'A serious fungal disease in cool, wet conditions',
                'symptoms': 'Water-soaked spots on leaves and stems, white mold on undersides',
                'prevention_tips': 'Use resistant varieties, reduce humidity, proper spacing',
                'suggested_pesticide': 'Copper fungicide or Metalaxyl',
                'treatment_duration': '10-21 days',
                'severity': 'High',
                'recommended_fertilizer': 'Calcium nitrate'
            },
            'Tomato Leaf Spot': {
                'crop_type': 'Tomato',
                'description': 'Bacterial leaf spot causing lesions',
                'symptoms': 'Small dark spots on leaves with yellow halos',
                'prevention_tips': 'Use disease-resistant seeds, avoid wet foliage, sanitize tools',
                'suggested_pesticide': 'Copper-based bactericide',
                'treatment_duration': '5-10 days',
                'severity': 'Low',
                'recommended_fertilizer': 'Balanced NPK fertilizer'
            },
            'Potato Early Blight': {
                'crop_type': 'Potato',
                'description': 'Fungal disease affecting potato foliage',
                'symptoms': 'Brown spots with concentric rings on lower leaves',
                'prevention_tips': 'Remove infected foliage, good drainage, crop rotation',
                'suggested_pesticide': 'Chlorothalonil or Mancozeb',
                'treatment_duration': '7-14 days',
                'severity': 'Medium',
                'recommended_fertilizer': 'Potassium-rich fertilizer'
            },
            'Potato Late Blight': {
                'crop_type': 'Potato',
                'description': 'Most destructive potato disease in cool, wet weather',
                'symptoms': 'Water-soaked spots spreading rapidly, white mold underneath',
                'prevention_tips': 'Use resistant varieties, destroy infected plants, proper ventilation',
                'suggested_pesticide': 'Metalaxyl-M or Cymoxanil',
                'treatment_duration': '14-21 days',
                'severity': 'High',
                'recommended_fertilizer': 'Calcium nitrate'
            },
            'Corn Common Rust': {
                'crop_type': 'Corn',
                'description': 'Fungal rust disease of corn',
                'symptoms': 'Reddish-brown pustules on leaves',
                'prevention_tips': 'Use resistant hybrids, adequate spacing, remove crop debris',
                'suggested_pesticide': 'Azoxystrobin or Propiconazole',
                'treatment_duration': '7-10 days',
                'severity': 'Low to Medium',
                'recommended_fertilizer': 'Nitrogen-rich fertilizer'
            },
            'Healthy Leaf': {
                'crop_type': 'General',
                'description': 'No disease detected',
                'symptoms': 'None - leaf is healthy',
                'prevention_tips': 'Continue regular maintenance and monitoring',
                'suggested_pesticide': 'No treatment needed',
                'treatment_duration': 'N/A',
                'severity': 'None',
                'recommended_fertilizer': 'Standard maintenance fertilizer'
            },
            'Unknown Disease': {
                'crop_type': 'Unknown',
                'description': 'Disease could not be identified',
                'symptoms': 'Please consult with agricultural expert',
                'prevention_tips': 'Maintain good crop hygiene',
                'suggested_pesticide': 'Consult expert before application',
                'treatment_duration': 'Unknown',
                'severity': 'Unknown',
                'recommended_fertilizer': 'Unknown'
            }
        }
