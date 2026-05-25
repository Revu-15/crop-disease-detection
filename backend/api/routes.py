from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from database.models import UploadHistory
from app import db

api_bp = Blueprint('api', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'status': 'ok',
        'message': 'Smart Crop Disease Detection API is running',
        'version': '1.0.0'
    }), 200

@api_bp.route('/predict', methods=['POST'])
def predict():
    """Predict disease from uploaded image"""
    try:
        # Check if file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format. Allowed: PNG, JPG, JPEG, GIF'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(upload_path)
        
        # Get disease detector from app context
        from app import disease_detector
        
        # Make prediction
        result = disease_detector.predict(upload_path)
        
        if not result['success']:
            return jsonify({'error': result.get('error', 'Prediction failed')}), 500
        
        # Save to database
        history = UploadHistory(
            filename=filename,
            original_filename=file.filename,
            disease_name=result['disease_name'],
            confidence=result['confidence'],
            image_path=f'/uploads/{filename}',
            treatment_given=False
        )
        db.session.add(history)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'prediction': {
                'disease_name': result['disease_name'],
                'confidence': result['confidence'],
                'image_path': f'/uploads/{filename}',
                'upload_id': history.id
            },
            'disease_info': result['disease_info']
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/history', methods=['GET'])
def get_history():
    """Get upload history"""
    try:
        limit = request.args.get('limit', 20, type=int)
        page = request.args.get('page', 1, type=int)
        
        history = UploadHistory.query.order_by(UploadHistory.upload_time.desc()) \
            .paginate(page=page, per_page=limit)
        
        return jsonify({
            'success': True,
            'data': [item.to_dict() for item in history.items],
            'total': history.total,
            'pages': history.pages,
            'current_page': page
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/history/<int:history_id>', methods=['GET'])
def get_history_item(history_id):
    """Get specific history item"""
    try:
        item = UploadHistory.query.get(history_id)
        
        if not item:
            return jsonify({'error': 'History item not found'}), 404
        
        # Get disease info
        from app import disease_detector
        disease_info = disease_detector.get_disease_info(item.disease_name)
        
        return jsonify({
            'success': True,
            'data': item.to_dict(),
            'disease_info': disease_info
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/history/delete/<int:history_id>', methods=['DELETE'])
def delete_history(history_id):
    """Delete history item"""
    try:
        item = UploadHistory.query.get(history_id)
        
        if not item:
            return jsonify({'error': 'History item not found'}), 404
        
        # Delete image file
        image_path = item.image_path.replace('/uploads/', '')
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_path)
        
        if os.path.exists(full_path):
            os.remove(full_path)
        
        db.session.delete(item)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'History item deleted'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/diseases', methods=['GET'])
def get_all_diseases():
    """Get all diseases in database"""
    try:
        from app import disease_detector
        
        diseases = list(disease_detector.disease_db.keys())
        
        return jsonify({
            'success': True,
            'diseases': diseases,
            'total': len(diseases)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/disease/<disease_name>', methods=['GET'])
def get_disease_details(disease_name):
    """Get specific disease information"""
    try:
        from app import disease_detector
        
        disease_info = disease_detector.get_disease_info(disease_name)
        
        if not disease_info:
            return jsonify({'error': 'Disease not found'}), 404
        
        return jsonify({
            'success': True,
            'disease_name': disease_name,
            'disease_info': disease_info
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
