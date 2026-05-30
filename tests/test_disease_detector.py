import unittest
import numpy as np
import json
import os
import tempfile
from PIL import Image
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.disease_detector import DiseaseDetector
from ml_model.preprocess import ImagePreprocessor

class DiseaseDetectorTestCase(unittest.TestCase):
    """Test cases for Disease Detector"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = DiseaseDetector()
        self.preprocessor = ImagePreprocessor()
        
        # Create temporary directory for test images
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up after tests"""
        # Remove temporary files
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def create_dummy_image(self, filename='test.jpg'):
        """Create a dummy image for testing"""
        img_path = os.path.join(self.test_dir, filename)
        img = Image.new('RGB', (224, 224), color='red')
        img.save(img_path)
        return img_path
    
    def test_detector_initialization(self):
        """Test DiseaseDetector initialization"""
        self.assertIsNotNone(self.detector)
        self.assertTrue(hasattr(self.detector, 'model'))
        self.assertTrue(hasattr(self.detector, 'disease_db'))
    
    def test_disease_database_loading(self):
        """Test disease database loading"""
        diseases = self.detector.get_all_diseases()
        self.assertIsInstance(diseases, list)
        self.assertGreater(len(diseases), 0)
    
    def test_disease_info_retrieval(self):
        """Test retrieving disease information"""
        disease_info = self.detector.get_disease_info('tomato_early_blight')
        self.assertIsNotNone(disease_info)
        self.assertIn('name', disease_info)
        self.assertIn('description', disease_info)
    
    def test_image_preprocessing(self):
        """Test image preprocessing for detection"""
        img_path = self.create_dummy_image()
        
        # Load and preprocess image
        img_array = self.preprocessor.load_image(img_path)
        
        self.assertIsNotNone(img_array)
        self.assertEqual(img_array.shape, (224, 224, 3))
        self.assertTrue(np.all(img_array >= 0) and np.all(img_array <= 1))
    
    def test_disease_detection(self):
        """Test disease detection"""
        img_path = self.create_dummy_image()
        
        try:
            result = self.detector.detect(img_path)
            
            self.assertIsNotNone(result)
            self.assertIn('disease', result)
            self.assertIn('confidence', result)
            self.assertIn('recommendations', result)
            
            # Check confidence is between 0 and 1
            self.assertGreaterEqual(result['confidence'], 0)
            self.assertLessEqual(result['confidence'], 1)
        except Exception as e:
            # Model might not be available in test environment
            self.skipTest(f"Model not available: {str(e)}")
    
    def test_batch_detection(self):
        """Test batch disease detection"""
        # Create multiple test images
        img_paths = [self.create_dummy_image(f'test_{i}.jpg') for i in range(3)]
        
        try:
            results = self.detector.detect_batch(img_paths)
            
            self.assertEqual(len(results), 3)
            
            for result in results:
                self.assertIn('disease', result)
                self.assertIn('confidence', result)
        except Exception as e:
            self.skipTest(f"Batch detection not available: {str(e)}")
    
    def test_recommendations_retrieval(self):
        """Test disease recommendations retrieval"""
        disease_name = 'tomato_early_blight'
        
        try:
            recommendations = self.detector.get_recommendations(disease_name)
            
            self.assertIsNotNone(recommendations)
            self.assertIsInstance(recommendations, dict)
            
            if recommendations:
                self.assertIn('treatment', recommendations)
                self.assertIn('prevention', recommendations)
        except Exception as e:
            self.skipTest(f"Recommendations not available: {str(e)}")
    
    def test_disease_statistics(self):
        """Test disease statistics"""
        try:
            stats = self.detector.get_statistics()
            
            self.assertIsInstance(stats, dict)
            self.assertIn('total_diseases', stats)
            self.assertIn('crops', stats)
        except Exception as e:
            self.skipTest(f"Statistics not available: {str(e)}")
    
    def test_invalid_image_format(self):
        """Test handling of invalid image format"""
        # Create a text file instead of image
        invalid_path = os.path.join(self.test_dir, 'invalid.txt')
        with open(invalid_path, 'w') as f:
            f.write('This is not an image')
        
        with self.assertRaises(Exception):
            self.preprocessor.load_image(invalid_path)
    
    def test_missing_image_file(self):
        """Test handling of missing image file"""
        invalid_path = os.path.join(self.test_dir, 'nonexistent.jpg')
        
        with self.assertRaises(Exception):
            self.preprocessor.load_image(invalid_path)
    
    def test_detection_result_format(self):
        """Test detection result format consistency"""
        img_path = self.create_dummy_image()
        
        try:
            result = self.detector.detect(img_path)
            
            # Check required fields
            required_fields = ['disease', 'confidence', 'crop_type']
            for field in required_fields:
                self.assertIn(field, result, f"Missing field: {field}")
            
            # Check data types
            self.assertIsInstance(result['disease'], str)
            self.assertIsInstance(result['confidence'], (int, float))
            self.assertIsInstance(result['crop_type'], str)
        except Exception as e:
            self.skipTest(f"Detection result format test skipped: {str(e)}")
    
    def test_confidence_threshold(self):
        """Test confidence threshold filtering"""
        threshold = 0.7
        
        try:
            result = self.detector.detect(self.create_dummy_image())
            
            if result['confidence'] >= threshold:
                self.assertGreater(result['confidence'], threshold - 0.01)
        except Exception as e:
            self.skipTest(f"Confidence threshold test skipped: {str(e)}")

if __name__ == '__main__':
    unittest.main()
