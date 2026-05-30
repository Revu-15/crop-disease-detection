# Contributing Guidelines

Thank you for your interest in contributing to the Crop Disease Detection project! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## 📜 Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of:
- Age, body size, disability, ethnicity, gender identity and expression
- Level of experience, nationality, personal appearance, race, religion
- Sexual identity and orientation

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Git
- GitHub account
- Text editor (VS Code recommended)

### Fork & Clone

```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/YOUR-USERNAME/crop-disease-detection.git

# Add upstream remote
git remote add upstream https://github.com/Revu-15/crop-disease-detection.git

# Verify remotes
git remote -v
```

## 💻 Development Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 3. Install Pre-commit Hooks

```bash
pre-commit install
```

### 4. Verify Setup

```bash
python -m pytest tests/ --cov
```

## ✏️ Making Changes

### Create Feature Branch

```bash
# Update main
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

### Branch Naming Convention

- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions
- `chore/` - Build/dependency updates

## 📝 Coding Standards

### Python Style Guide (PEP 8)

```python
# Good: Clear, descriptive names
def predict_disease_from_image(image_path: str) -> dict:
    """
    Predict disease from plant leaf image.
    
    Args:
        image_path: Path to the image file
    
    Returns:
        Dictionary with prediction results
    """
    # Implementation
    pass

# Bad: Unclear names
def pred(img):
    # Implementation
    pass
```

### Type Hints

```python
from typing import List, Dict, Optional

def process_images(images: List[str]) -> Dict[str, float]:
    """Process multiple images and return results."""
    pass

def get_user(user_id: int) -> Optional[User]:
    """Get user by ID, returns None if not found."""
    pass
```

### Docstring Format

```python
def classify_disease(image: np.ndarray) -> str:
    """
    Classify disease from image array.
    
    Args:
        image: Input image as numpy array (224, 224, 3)
    
    Returns:
        Disease classification string
    
    Raises:
        ValueError: If image shape is incorrect
        
    Example:
        >>> image = load_image('leaf.jpg')
        >>> disease = classify_disease(image)
        >>> print(disease)
        'Early Blight'
    """
    if image.shape != (224, 224, 3):
        raise ValueError("Image must be 224x224x3")
    
    # Implementation
    return disease
```

### Code Formatting

```bash
# Format with Black
black backend/ ml_model/ tests/

# Check with Flake8
flake8 backend/ ml_model/ tests/

# Sort imports with isort
isort backend/ ml_model/ tests/
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

def predict(image_path: str):
    logger.info(f"Processing image: {image_path}")
    try:
        result = model.predict(image_path)
        logger.debug(f"Prediction result: {result}")
        return result
    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}", exc_info=True)
        raise
```

## 🧪 Testing

### Write Tests

```python
# tests/test_disease_classifier.py
import unittest
from unittest.mock import patch, MagicMock
from ml_model.classifier import DiseaseClassifier

class TestDiseaseClassifier(unittest.TestCase):
    """Test disease classification."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.classifier = DiseaseClassifier()
    
    def test_classify_valid_image(self):
        """Test classification with valid image."""
        # Arrange
        image = create_test_image()
        
        # Act
        result = self.classifier.classify(image)
        
        # Assert
        self.assertIn('disease', result)
        self.assertIn('confidence', result)
        self.assertGreaterEqual(result['confidence'], 0)
        self.assertLessEqual(result['confidence'], 1)
    
    @patch('ml_model.classifier.load_model')
    def test_model_not_loaded(self, mock_load):
        """Test handling when model fails to load."""
        mock_load.side_effect = Exception("Model not found")
        
        with self.assertRaises(Exception):
            DiseaseClassifier()
```

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage
pytest tests/ --cov=backend --cov=ml_model --cov-report=html

# Run with markers
pytest tests/ -m slow -v
```

### Test Coverage Requirements

- Minimum 80% code coverage
- 100% coverage for critical functions
- All public methods must have tests

## 📋 Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Build/dependency updates

### Examples

```bash
# Good commits
git commit -m "feat(api): add batch prediction endpoint"
git commit -m "fix(model): improve image preprocessing accuracy"
git commit -m "docs: update API documentation"

# Bad commits
git commit -m "updated code"
git commit -m "fixed stuff"
git commit -m "WIP"
```

## 🔄 Pull Request Process

### Before Creating PR

1. **Update from upstream**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests**
   ```bash
   pytest tests/ -v --cov
   ```

3. **Format code**
   ```bash
   black .
   flake8 .
   isort .
   ```

4. **Check documentation**
   - Docstrings added/updated
   - README updated if needed
   - Examples provided for new features

### Create Pull Request

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create PR on GitHub**
   - Use clear title
   - Reference related issues
   - Describe changes clearly

### PR Title Format

```
[Type] Short description

Examples:
[Feature] Add batch prediction endpoint
[Fix] Fix image preprocessing bug
[Docs] Update API documentation
```

### PR Description Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Related Issues
Fixes #123

## Testing
- [ ] Added/updated tests
- [ ] All tests passing
- [ ] Coverage maintained

## Screenshots (if applicable)
Include screenshots for UI changes

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes
```

### Review Process

1. **Code Review**
   - Maintainers review code quality
   - Functionality assessment
   - Performance considerations

2. **CI/CD Checks**
   - Tests must pass
   - Coverage maintained
   - Code style validated

3. **Approval**
   - Requires 2 approvals for main
   - 1 approval for other branches

4. **Merge**
   - Squash commits if needed
   - Delete branch after merge

## 🐛 Reporting Issues

### Issue Template

```markdown
## Description
Clear description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Ubuntu 20.04
- Python: 3.9
- Version: 1.0.0

## Screenshots
If applicable

## Additional Context
Any other relevant information
```

### Issue Labels

- `bug`: Bug report
- `feature`: Feature request
- `documentation`: Documentation issue
- `good-first-issue`: Good for newcomers
- `help-wanted`: Need assistance
- `in-progress`: Being worked on
- `priority-high`: High priority

## 📞 Support

### Questions?

- GitHub Discussions for Q&A
- Email: support@crop-disease-detection.com
- Issues: Use issue template for bugs

### Useful Resources

- [Python PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Commit Message Guidelines](https://www.conventionalcommits.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

## 🎉 Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

---

**Thank you for contributing!** 🙏

For any questions or concerns, please reach out to the maintainers.

**Last Updated**: 2026-05-30
