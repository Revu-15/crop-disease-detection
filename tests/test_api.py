import unittest
import json
import os
from flask import Flask
from backend.app import create_app
from backend.models import db

class APITestCase(unittest.TestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_api_root(self):
        """Test API root endpoint"""
        response = self.client.get('/api')
        self.assertEqual(response.status_code, 200)
    
    def test_get_diseases(self):
        """Test get diseases endpoint"""
        response = self.client.get('/api/diseases')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('diseases', data)
    
    def test_disease_info(self):
        """Test disease info endpoint"""
        response = self.client.get('/api/diseases/tomato_early_blight')
        self.assertEqual(response.status_code, 200)
    
    def test_predict_missing_file(self):
        """Test predict endpoint without file"""
        response = self.client.post('/api/predict')
        self.assertEqual(response.status_code, 400)
    
    def test_predict_invalid_file(self):
        """Test predict endpoint with invalid file"""
        data = {
            'file': (None, 'test.txt')
        }
        response = self.client.post('/api/predict', data=data)
        self.assertEqual(response.status_code, 400)
    
    def test_cors_headers(self):
        """Test CORS headers"""
        response = self.client.options('/api/health')
        self.assertIn('Access-Control-Allow-Origin', response.headers)
    
    def test_get_model_info(self):
        """Test model info endpoint"""
        response = self.client.get('/api/model/info')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('model_name', data)
        self.assertIn('version', data)

if __name__ == '__main__':
    unittest.main()
