# Contributing Guidelines

Thank you for your interest in contributing to the Smart Crop Disease Detection System!

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## How to Contribute

### 1. Fork the Repository

```bash
git clone https://github.com/YOUR-USERNAME/crop-disease-detection.git
cd crop-disease-detection
git remote add upstream https://github.com/Revu-15/crop-disease-detection.git
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 3. Make Changes

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Keep functions small and focused

### 4. Test Your Changes

```bash
# Run tests
pytest backend/

# Check code style
flake8 backend/
black backend/

# Manual testing
python backend/app.py
```

### 5. Commit with Clear Messages

```bash
git add .
git commit -m "feat: add new feature description"
git commit -m "fix: resolve issue description"
git commit -m "docs: update documentation"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types:
- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation update
- **style:** Code style changes (formatting, etc.)
- **refactor:** Code refactoring
- **perf:** Performance improvement
- **test:** Test addition/modification
- **chore:** Build, dependency, or tooling changes

### Examples:
```
feat(api): add batch prediction endpoint
fix(database): resolve connection timeout issue
docs(readme): update installation instructions
refactor(frontend): simplify upload form logic
```

## Pull Request Process

1. **Title:** Clear, descriptive title
2. **Description:** Explain what and why
3. **Related Issues:** Reference relevant issues
4. **Testing:** Describe tests performed
5. **Screenshots:** Include for UI changes

### PR Template:
```markdown
## Description

Brief description of changes.

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing

Describe testing performed.

## Checklist

- [ ] Code follows style guidelines
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
```

## Areas for Contribution

### High Priority
- [ ] ML model improvements
- [ ] Performance optimization
- [ ] Security enhancements
- [ ] Bug fixes

### Medium Priority
- [ ] UI/UX improvements
- [ ] Documentation
- [ ] Testing coverage
- [ ] API enhancements

### Nice to Have
- [ ] Mobile app
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] IoT integration

## Development Setup

See [SETUP.md](SETUP.md) for detailed setup instructions.

## Code Style

### Python (Backend)

```python
# Good
def predict_disease(image_path: str) -> dict:
    """Predict disease from image.
    
    Args:
        image_path: Path to image file
        
    Returns:
        Dictionary with prediction results
    """
    result = disease_detector.predict(image_path)
    return result

# Bad
def predict(img):
    # predict disease
    result = disease_detector.predict(img)
    return result
```

### JavaScript (Frontend)

```javascript
// Good
async function uploadImage(file) {
    const formData = new FormData();
    formData.append('image', file);
    
    const response = await fetch('/api/predict', {
        method: 'POST',
        body: formData
    });
    
    return response.json();
}

// Bad
function upload(f) {
    var fd = new FormData();
    fd.append('image', f);
    fetch('/api/predict', {method: 'POST', body: fd});
}
```

## Documentation Standards

- Add docstrings to all functions
- Update README for major changes
- Add API documentation for new endpoints
- Include examples in documentation

## Testing

### Unit Tests

```python
# backend/tests/test_disease_detector.py
import pytest
from api.disease_detector import DiseaseDetector

def test_disease_detection():
    detector = DiseaseDetector(app)
    result = detector.predict('test_image.jpg')
    assert result['success'] == True
    assert 'disease_name' in result
```

### Running Tests

```bash
# All tests
pytest

# Specific test
pytest backend/tests/test_disease_detector.py

# With coverage
pytest --cov=backend backend/
```

## Reporting Bugs

### Issue Template

```markdown
## Bug Description

Clear description of the bug.

## Steps to Reproduce

1. Step one
2. Step two
3. ...

## Expected Behavior

What should happen.

## Actual Behavior

What actually happens.

## Environment

- OS: Windows/macOS/Linux
- Python: 3.8/3.9/3.10
- Browser: Chrome/Firefox/Safari

## Screenshots

If applicable, add screenshots.
```

## Review Process

1. Automated checks pass (CI/CD)
2. Code review by maintainers
3. Approval and merge
4. Deployment to production

## Questions?

Open an issue with the question label or contact maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing!** 🎉
