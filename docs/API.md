# API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, the API does not require authentication. In production, implement JWT or OAuth2.

## Endpoints

### 1. Health Check
Verify API is running.

**Request:**
```
GET /api/health
```

**Response:**
```json
{
  "status": "ok",
  "message": "Smart Crop Disease Detection API is running",
  "version": "1.0.0"
}
```

---

### 2. Predict Disease
Upload an image and get disease prediction.

**Request:**
```
POST /api/predict
Content-Type: multipart/form-data

Form Data:
  - image: <file>  (JPG, PNG, GIF. Max 16MB)
```

**Response (Success):**
```json
{
  "success": true,
  "prediction": {
    "disease_name": "Tomato Early Blight",
    "confidence": 0.9543,
    "image_path": "/uploads/20240525_120530_leaf.jpg",
    "upload_id": 1
  },
  "disease_info": {
    "crop_type": "Tomato",
    "description": "A fungal disease...",
    "symptoms": "Brown spots with concentric rings...",
    "prevention_tips": "Remove infected leaves...",
    "suggested_pesticide": "Chlorothalonil or Mancozeb",
    "treatment_duration": "7-14 days",
    "severity": "Medium",
    "recommended_fertilizer": "Potassium-rich fertilizer"
  }
}
```

**Response (Error):**
```json
{
  "error": "No image file provided"
}
```

**Status Codes:**
- `200` - Success
- `400` - Bad request (missing/invalid file)
- `500` - Server error

---

### 3. Get Upload History
Retrieve all previous uploads with pagination.

**Request:**
```
GET /api/history?limit=20&page=1
```

**Query Parameters:**
- `limit` (optional): Number of items per page (default: 20, max: 100)
- `page` (optional): Page number (default: 1)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "filename": "20240525_120530_leaf.jpg",
      "original_filename": "leaf.jpg",
      "disease_name": "Tomato Early Blight",
      "confidence": 0.9543,
      "upload_time": "2024-05-25 12:05:30",
      "image_path": "/uploads/20240525_120530_leaf.jpg",
      "treatment_given": false
    }
  ],
  "total": 5,
  "pages": 1,
  "current_page": 1
}
```

---

### 4. Get Specific History Item
Retrieve details of a specific upload.

**Request:**
```
GET /api/history/<history_id>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "filename": "20240525_120530_leaf.jpg",
    "original_filename": "leaf.jpg",
    "disease_name": "Tomato Early Blight",
    "confidence": 0.9543,
    "upload_time": "2024-05-25 12:05:30",
    "image_path": "/uploads/20240525_120530_leaf.jpg",
    "treatment_given": false
  },
  "disease_info": {
    "crop_type": "Tomato",
    "description": "A fungal disease...",
    "symptoms": "Brown spots with concentric rings...",
    "prevention_tips": "Remove infected leaves...",
    "suggested_pesticide": "Chlorothalonil or Mancozeb",
    "treatment_duration": "7-14 days",
    "severity": "Medium",
    "recommended_fertilizer": "Potassium-rich fertilizer"
  }
}
```

---

### 5. Delete History Item
Remove an upload from history.

**Request:**
```
DELETE /api/history/delete/<history_id>
```

**Response:**
```json
{
  "success": true,
  "message": "History item deleted"
}
```

---

### 6. Get All Diseases
List all supported diseases.

**Request:**
```
GET /api/diseases
```

**Response:**
```json
{
  "success": true,
  "diseases": [
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Tomato Leaf Spot",
    "Potato Early Blight",
    "Potato Late Blight",
    "Corn Common Rust",
    "Healthy Leaf"
  ],
  "total": 7
}
```

---

### 7. Get Disease Details
Retrieve detailed information about a specific disease.

**Request:**
```
GET /api/disease/<disease_name>
```

**Example:**
```
GET /api/disease/Tomato%20Early%20Blight
```

**Response:**
```json
{
  "success": true,
  "disease_name": "Tomato Early Blight",
  "disease_info": {
    "crop_type": "Tomato",
    "description": "A fungal disease affecting tomato leaves...",
    "symptoms": "Brown circular spots with concentric rings...",
    "prevention_tips": "Remove infected leaves, improve air circulation...",
    "suggested_pesticide": "Chlorothalonil, Mancozeb, or Copper sulfate",
    "treatment_duration": "7-14 days",
    "severity": "Medium",
    "recommended_fertilizer": "Potassium-rich fertilizer (Potash)",
    "spray_schedule": "Every 7-10 days starting from early stages"
  }
}
```

---

## Error Codes

| Code | Message | Cause |
|------|---------|-------|
| 400 | No image file provided | Missing file in request |
| 400 | No file selected | Empty file selection |
| 400 | Invalid file format | Non-image file uploaded |
| 404 | History item not found | Invalid history ID |
| 404 | Disease not found | Invalid disease name |
| 404 | Resource not found | Invalid endpoint |
| 500 | Prediction failed | ML model error |
| 500 | Internal server error | Server-side error |

## Rate Limiting

Currently not implemented. For production, add rate limiting to prevent abuse:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/predict', methods=['POST'])
@limiter.limit("30 per hour")
def predict():
    ...
```

## CORS Configuration

Allowed origins (configured in `config.py`):
- Development: `http://localhost:3000`, `http://localhost:5000`, `http://localhost:8000`
- Production: Update to your domain

## Example cURL Requests

### Health Check
```bash
curl -X GET http://localhost:5000/api/health
```

### Predict Disease
```bash
curl -X POST http://localhost:5000/api/predict \
  -F "image=@path/to/leaf.jpg"
```

### Get History
```bash
curl -X GET "http://localhost:5000/api/history?limit=10&page=1"
```

### Get Disease Details
```bash
curl -X GET "http://localhost:5000/api/disease/Tomato%20Early%20Blight"
```

## WebSocket Support (Future)

Planned for real-time prediction updates:
```javascript
const socket = io('http://localhost:5000');
socket.on('prediction_update', (data) => {
    console.log('Prediction:', data);
});
```

---

**Last Updated:** May 2026  
**Version:** 1.0.0
