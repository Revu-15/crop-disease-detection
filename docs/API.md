# API Documentation

Complete REST API reference for the Crop Disease Detection system.

## 📋 Table of Contents

- [Base URL](#base-url)
- [Authentication](#authentication)
- [Disease Endpoints](#disease-endpoints)
- [Prediction Endpoints](#prediction-endpoints)
- [User Endpoints](#user-endpoints)
- [Response Format](#response-format)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)

## 🌐 Base URL

```
http://localhost:5000/api
https://api.crop-disease.com/api  (Production)
```

## 🔐 Authentication

### Authentication Methods

#### 1. API Key
```bash
Authorization: Bearer YOUR_API_KEY
```

#### 2. JWT Token
```bash
Authorization: Bearer YOUR_JWT_TOKEN
```

#### 3. Session Cookie
```bash
Cookie: session=YOUR_SESSION_ID
```

### Get API Key

```http
POST /api/auth/apikey
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "api_key": "sk_live_51HeyMzI0ZzF5eXl6...",
  "expires_at": "2026-05-30T10:00:00Z"
}
```

### JWT Login

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "username": "john_doe"
  }
}
```

## 🏥 Disease Endpoints

### Get All Diseases

```http
GET /api/diseases
Authorization: Bearer YOUR_API_KEY
```

**Query Parameters:**
- `crop_type` (optional): Filter by crop type
- `page` (optional): Pagination page (default: 1)
- `per_page` (optional): Items per page (default: 30)

**Response:**
```json
{
  "success": true,
  "data": {
    "diseases": [
      {
        "id": "disease_001",
        "name": "Early Blight",
        "scientific_name": "Alternaria solani",
        "crop_type": "Tomato",
        "severity": "high",
        "description": "Fungal disease affecting leaves and stems..."
      },
      {
        "id": "disease_002",
        "name": "Late Blight",
        "scientific_name": "Phytophthora infestans",
        "crop_type": "Tomato",
        "severity": "critical",
        "description": "Destructive fungal disease..."
      }
    ],
    "total": 38,
    "page": 1,
    "per_page": 30
  }
}
```

### Get Disease Details

```http
GET /api/diseases/{disease_id}
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "disease_001",
    "name": "Early Blight",
    "scientific_name": "Alternaria solani",
    "crop_type": "Tomato",
    "severity": "high",
    "description": "Fungal disease affecting leaves and stems",
    "symptoms": [
      "Brown or black spots on leaves",
      "Concentric rings within spots",
      "Yellow halo around spots",
      "Spots may have a target-like appearance"
    ],
    "causes": [
      "Fungal pathogen Alternaria solani",
      "Warm, humid weather",
      "Poor air circulation",
      "Overhead watering"
    ],
    "treatment": {
      "chemical": [
        "Copper fungicide (Bordeaux mixture)",
        "Chlorothalonil",
        "Mancozeb"
      ],
      "organic": [
        "Baking soda spray (1 tbsp per gallon)",
        "Neem oil",
        "Sulfur dust"
      ],
      "cultural": [
        "Remove infected leaves",
        "Improve air circulation",
        "Water at soil level",
        "Sanitize tools"
      ]
    },
    "prevention": [
      "Use resistant varieties",
      "Crop rotation",
      "Proper spacing",
      "Remove plant debris",
      "Avoid overhead watering"
    ],
    "mortality_rate": "15-20%",
    "recovery_time": "7-14 days with treatment"
  }
}
```

### Get Disease Recommendations

```http
GET /api/diseases/{disease_id}/recommendations
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "success": true,
  "data": {
    "disease_id": "disease_001",
    "disease_name": "Early Blight",
    "recommendations": {
      "immediate": [
        "Remove infected leaves immediately",
        "Improve air circulation",
        "Apply fungicide"
      ],
      "short_term": [
        "Monitor daily for new symptoms",
        "Continue fungicide application",
        "Water early morning only"
      ],
      "long_term": [
        "Practice crop rotation",
        "Use disease-resistant varieties",
        "Implement integrated pest management"
      ]
    },
    "estimated_cost": "$50-150 per plant",
    "recovery_probability": "85%"
  }
}
```

## 🔮 Prediction Endpoints

### Single Image Prediction

```http
POST /api/predict
Authorization: Bearer YOUR_API_KEY
Content-Type: multipart/form-data

{
  "file": <image_file>,
  "confidence_threshold": 0.7 (optional)
}
```

**Supported Formats:**
- JPG, JPEG
- PNG
- BMP
- GIF
- TIFF

**File Size:** Max 10MB

**Response:**
```json
{
  "success": true,
  "data": {
    "prediction_id": "pred_123456",
    "image_name": "leaf_sample.jpg",
    "upload_time": "2026-05-30T10:15:30Z",
    "analysis": {
      "detected_disease": "Early Blight",
      "disease_id": "disease_001",
      "crop_type": "Tomato",
      "confidence": 0.94,
      "confidence_percentage": "94%",
      "alternate_diseases": [
        {
          "name": "Septoria Leaf Spot",
          "confidence": 0.05,
          "confidence_percentage": "5%"
        },
        {
          "name": "Healthy",
          "confidence": 0.01,
          "confidence_percentage": "1%"
        }
      ]
    },
    "recommendations": {
      "treatment": [
        "Apply copper fungicide",
        "Remove infected leaves",
        "Improve ventilation"
      ],
      "prevention": [
        "Use resistant varieties",
        "Implement crop rotation"
      ]
    },
    "severity": {
      "level": "high",
      "affected_area": "25%",
      "progression_rate": "fast"
    },
    "suggested_actions": [
      "Take immediate treatment measures",
      "Monitor plant daily",
      "Consider chemical intervention"
    ]
  }
}
```

### Batch Prediction

```http
POST /api/predict/batch
Authorization: Bearer YOUR_API_KEY
Content-Type: multipart/form-data

{
  "files": [<image_file_1>, <image_file_2>, ...],
  "max_results": 100 (optional)
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "batch_id": "batch_123456",
    "total_images": 3,
    "processed_images": 3,
    "failed_images": 0,
    "processing_time_ms": 450,
    "predictions": [
      {
        "image_name": "leaf1.jpg",
        "disease": "Early Blight",
        "confidence": 0.94
      },
      {
        "image_name": "leaf2.jpg",
        "disease": "Late Blight",
        "confidence": 0.89
      },
      {
        "image_name": "leaf3.jpg",
        "disease": "Healthy",
        "confidence": 0.98
      }
    ],
    "summary": {
      "diseases_detected": 2,
      "healthy_plants": 1,
      "average_confidence": 0.94
    }
  }
}
```

### Get Prediction History

```http
GET /api/predictions
Authorization: Bearer YOUR_API_KEY

Query Parameters:
- user_id (optional): Filter by user
- disease_id (optional): Filter by disease
- start_date (optional): Filter from date (ISO 8601)
- end_date (optional): Filter to date (ISO 8601)
- page (optional): Page number (default: 1)
- per_page (optional): Items per page (default: 20)
```

**Response:**
```json
{
  "success": true,
  "data": {
    "predictions": [
      {
        "prediction_id": "pred_123456",
        "image_name": "leaf_sample.jpg",
        "disease": "Early Blight",
        "confidence": 0.94,
        "timestamp": "2026-05-30T10:15:30Z",
        "status": "completed"
      }
    ],
    "total": 150,
    "page": 1,
    "per_page": 20
  }
}
```

## 👤 User Endpoints

### Create User

```http
POST /api/users
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password_123",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": "user_123",
    "username": "john_doe",
    "email": "john@example.com",
    "created_at": "2026-05-30T10:00:00Z"
  }
}
```

### Get User Profile

```http
GET /api/users/profile
Authorization: Bearer YOUR_API_KEY
```

**Response:**
```json
{
  "success": true,
  "data": {
    "user_id": "user_123",
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "created_at": "2026-05-30T10:00:00Z",
    "predictions_count": 45,
    "subscription_plan": "premium"
  }
}
```

### Update User Profile

```http
PUT /api/users/profile
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json

{
  "full_name": "John Doe",
  "phone": "+1234567890"
}
```

## 📊 Health & Info Endpoints

### API Health Check

```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-05-30T10:30:00Z",
  "uptime_seconds": 86400,
  "database": "connected",
  "model": "loaded"
}
```

### API Info

```http
GET /api/info
```

**Response:**
```json
{
  "name": "Crop Disease Detection API",
  "version": "1.0.0",
  "description": "AI-powered crop disease detection system",
  "endpoints": 25,
  "model_version": "v2.1.0",
  "model_accuracy": "95.2%",
  "supported_crops": 12,
  "total_diseases": 38,
  "documentation_url": "https://docs.crop-disease.com"
}
```

## 📋 Response Format

### Success Response
```json
{
  "success": true,
  "data": {
    // Response data
  },
  "timestamp": "2026-05-30T10:00:00Z"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Invalid image format",
    "details": "Only JPG, PNG, BMP, GIF, and TIFF formats are supported"
  },
  "timestamp": "2026-05-30T10:00:00Z"
}
```

## ⚠️ Error Handling

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Rate Limit Exceeded |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

### Error Codes

```
INVALID_INPUT: Invalid input parameters
UNAUTHORIZED: Authentication failed
FORBIDDEN: Access denied
NOT_FOUND: Resource not found
FILE_TOO_LARGE: File exceeds size limit
INVALID_FILE_FORMAT: Unsupported file format
MODEL_ERROR: Model inference failed
DATABASE_ERROR: Database operation failed
RATE_LIMIT: API rate limit exceeded
INTERNAL_ERROR: Internal server error
```

## ⏱️ Rate Limiting

- **Free Plan**: 100 requests/hour
- **Pro Plan**: 1,000 requests/hour
- **Enterprise Plan**: Unlimited

### Rate Limit Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1622390400
```

## 📝 Examples

### Complete Workflow Example

```bash
# 1. Get API Key
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# 2. List Available Diseases
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/diseases

# 3. Get Disease Details
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/diseases/disease_001

# 4. Make Prediction
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@leaf_image.jpg" \
  http://localhost:5000/api/predict

# 5. Get Prediction History
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/predictions
```

### Python Example

```python
import requests

API_URL = "http://localhost:5000/api"
API_KEY = "your_api_key"

# Predict disease
with open("leaf_image.jpg", "rb") as f:
    files = {"file": f}
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.post(
        f"{API_URL}/predict",
        files=files,
        headers=headers
    )
    
result = response.json()
print(f"Disease: {result['data']['analysis']['detected_disease']}")
print(f"Confidence: {result['data']['analysis']['confidence_percentage']}")
```

---

**Last Updated**: 2026-05-30
