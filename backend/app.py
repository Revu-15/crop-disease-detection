from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from config import config

# Initialize Flask app
app = Flask(__name__, template_folder='../frontend', static_folder='../static')
app.config.from_object(config[os.getenv('FLASK_ENV', 'development')])

# Initialize extensions
db = SQLAlchemy(app)
CORS(app, origins=app.config['CORS_ORIGINS'])

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Import models and routes
from database.models import UploadHistory, Disease
from api.routes import api_bp
from api.disease_detector import DiseaseDetector

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')

# Initialize disease detector
disease_detector = DiseaseDetector(app)

@app.route('/')
def home():
    """Serve home page"""
    return render_template('index.html')

@app.route('/upload')
def upload_page():
    """Serve upload page"""
    return render_template('upload.html')

@app.route('/result')
def result_page():
    """Serve result page"""
    return render_template('result.html')

@app.route('/history')
def history_page():
    """Serve history page"""
    return render_template('history.html')

@app.shell_context_processor
def make_shell_context():
    """Make database objects available in shell"""
    return {'db': db, 'UploadHistory': UploadHistory, 'Disease': Disease}

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
