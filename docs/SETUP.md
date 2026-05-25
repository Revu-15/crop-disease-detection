# Setup Guide

## System Requirements

- **OS:** Windows, macOS, or Linux
- **Python:** 3.8 or higher
- **RAM:** Minimum 4GB (8GB recommended)
- **Storage:** 2GB free space (for model and dependencies)

## Step-by-Step Installation

### 1. Clone Repository

```bash
git clone https://github.com/Revu-15/crop-disease-detection.git
cd crop-disease-detection
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r backend/requirements.txt
```

**Installation time:** ~10-15 minutes (first time)

### 4. Environment Configuration

Create `.env` file from template:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```
FLASK_ENV=development
FLASK_APP=backend/app.py
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///database/crop_diseases.db
```

### 5. Initialize Database

```bash
cd backend
python
```

In Python shell:
```python
from app import app, db
with app.app_context():
    db.create_all()
    print("Database initialized!")
exit()
```

Or use one-liner:
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"
```

### 6. Download/Place ML Model

The system works without a model (uses mock predictions), but for real predictions:

1. Train a model or download pre-trained model
2. Place in: `backend/models/crop_disease_model.h5`

**Option A: Using Pre-trained Model**
```bash
# Download model (example - replace with actual URL)
wget https://example.com/crop_disease_model.h5 -O backend/models/crop_disease_model.h5
```

**Option B: Train Your Own**
```bash
cd backend
python ../ml_model/train.py --dataset /path/to/dataset --epochs 50
```

### 7. Run Application

```bash
python backend/app.py
```

**Output:**
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

Access application at: **http://localhost:5000**

## Verification

Check if everything is working:

```bash
# Test API health
curl http://localhost:5000/api/health

# Should return:
# {"status": "ok", "message": "..."}
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'tensorflow'"

**Solution:**
```bash
pip install tensorflow==2.13.0
```

### Issue: "Address already in use"

**Solution:** Change port in `backend/app.py`:
```python
if __name__ == '__main__':
    app.run(port=5001)  # Changed from 5000
```

### Issue: "Database is locked"

**Solution:** Delete and recreate database:
```bash
rm backend/database/crop_diseases.db
python backend/app.py
```

### Issue: "No module named 'flask'"

**Solution:** Ensure virtual environment is activated:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Then install again
pip install -r backend/requirements.txt
```

### Issue: "Model not found" warning

**Solution:** This is normal. The system uses mock predictions without a model.
To use real predictions, add a trained model to `backend/models/`

## Development Setup

### Install Development Tools

```bash
pip install pytest pytest-cov black flake8 jupyter notebook
```

### Enable Debug Mode

Edit `backend/config.py`:
```python
class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
```

### Run Tests

```bash
pytest backend/
```

### Code Formatting

```bash
black backend/
flake8 backend/
```

## Production Setup

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment instructions.

## File Structure After Setup

```
crop-disease-detection/
├── venv/                    # Virtual environment (created)
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── database/
│   │   └── crop_diseases.db  # Created after step 5
│   ├── models/
│   │   └── crop_disease_model.h5  # Add in step 6
│   ├── uploads/              # Created automatically
│   ├── api/
│   ├── database/
│   └── data/
├── frontend/
├── static/
├── .env                      # Created from .env.example
└── README.md
```

## Next Steps

1. **Try the UI:**
   - Visit http://localhost:5000
   - Upload a crop leaf image
   - Check results and history

2. **Explore the Code:**
   - Check `backend/app.py` for Flask setup
   - Check `frontend/js/` for UI logic
   - Check `backend/api/routes.py` for API endpoints

3. **Train Custom Model:**
   - Use your own dataset
   - Follow `ml_model/train.py` instructions
   - Replace model file

4. **Deploy to Production:**
   - See [DEPLOYMENT.md](DEPLOYMENT.md)
   - Use Heroku, AWS, or DigitalOcean

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [TensorFlow Setup Guide](https://www.tensorflow.org/install)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)

---

**Estimated Total Setup Time:** 20-30 minutes

