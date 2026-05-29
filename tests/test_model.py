import unittest
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ml_model.preprocess import ImagePreprocessor
from ml_model.evaluate import ModelEvaluator

class ModelTestCase(unittest.TestCase):
    """Test cases for ML model"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.preprocessor = ImagePreprocessor()
        self.evaluator = ModelEvaluator()
        
        # Create a simple test model
        self.model = Sequential([
            Dense(64, activation='relu', input_shape=(224*224*3,)),
            Dense(32, activation='relu'),
            Dense(10, activation='softmax')
        ])
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    def test_image_loading(self):
        """Test image loading and preprocessing"""
        # Create a dummy image array
        dummy_image = np.random.rand(224, 224, 3)
        
        # Test normalization
        normalized = self.preprocessor.normalize_image(dummy_image)
        self.assertTrue(np.all(normalized >= 0) and np.all(normalized <= 1))
    
    def test_image_normalization(self):
        """Test image normalization"""
        image = np.random.rand(224, 224, 3)
        normalized = self.preprocessor.normalize_image(image)
        
        self.assertEqual(normalized.shape, image.shape)
        self.assertLessEqual(np.max(normalized), 1.0)
        self.assertGreaterEqual(np.min(normalized), 0.0)
    
    def test_feature_extraction(self):
        """Test feature extraction"""
        # Create a dummy image
        dummy_image = np.random.rand(224, 224, 3)
        
        # Extract features
        features = self.preprocessor.extract_features(dummy_image)
        
        # Check feature shape
        self.assertEqual(len(features), 6)
        self.assertTrue(all(isinstance(f, (int, float, np.number)) for f in features))
    
    def test_model_prediction(self):
        """Test model prediction"""
        # Create dummy test data
        X_test = np.random.rand(10, 224*224*3).astype(np.float32)
        
        # Make predictions
        predictions = self.model.predict(X_test, verbose=0)
        
        # Check predictions shape and values
        self.assertEqual(predictions.shape, (10, 10))
        self.assertTrue(np.all(predictions >= 0) and np.all(predictions <= 1))
        # Check that predictions sum to 1 (softmax)
        self.assertTrue(np.allclose(np.sum(predictions, axis=1), 1))
    
    def test_model_evaluation(self):
        """Test model evaluation"""
        # Create dummy test data
        X_test = np.random.rand(10, 224*224*3).astype(np.float32)
        y_test = np.eye(10)[np.random.randint(0, 10, 10)]  # One-hot encoded
        
        # Evaluate model
        metrics = self.evaluator.evaluate_model(self.model, X_test, y_test)
        
        # Check metrics exist
        self.assertIn('accuracy', metrics)
        self.assertIn('precision', metrics)
        self.assertIn('recall', metrics)
        self.assertIn('f1', metrics)
        self.assertIn('confusion_matrix', metrics)
        
        # Check metric ranges
        self.assertGreaterEqual(metrics['accuracy'], 0)
        self.assertLessEqual(metrics['accuracy'], 1)
    
    def test_per_class_evaluation(self):
        """Test per-class evaluation"""
        # Create dummy test data
        X_test = np.random.rand(10, 224*224*3).astype(np.float32)
        y_test = np.eye(10)[np.random.randint(0, 10, 10)]
        
        class_names = [f'Class_{i}' for i in range(10)]
        
        # Evaluate per class
        per_class_metrics = self.evaluator.evaluate_per_class(self.model, X_test, y_test, class_names)
        
        # Check output format
        self.assertIsInstance(per_class_metrics, dict)
        for class_name, metrics in per_class_metrics.items():
            self.assertIn('accuracy', metrics)
            self.assertIn('samples', metrics)

if __name__ == '__main__':
    unittest.main()
