from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import db

class UploadHistory(db.Model):
    """Model for storing upload history"""
    __tablename__ = 'upload_history'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    disease_name = db.Column(db.String(255), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    image_path = db.Column(db.String(500), nullable=False)
    treatment_given = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'disease_name': self.disease_name,
            'confidence': round(self.confidence, 2),
            'upload_time': self.upload_time.strftime('%Y-%m-%d %H:%M:%S'),
            'image_path': self.image_path,
            'treatment_given': self.treatment_given
        }

class Disease(db.Model):
    """Model for storing disease information"""
    __tablename__ = 'diseases'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    crop_type = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    prevention_tips = db.Column(db.Text, nullable=False)
    suggested_pesticide = db.Column(db.String(500), nullable=False)
    treatment_duration = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(50), nullable=False)  # Low, Medium, High
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'crop_type': self.crop_type,
            'description': self.description,
            'symptoms': self.symptoms,
            'prevention_tips': self.prevention_tips,
            'suggested_pesticide': self.suggested_pesticide,
            'treatment_duration': self.treatment_duration,
            'severity': self.severity
        }
