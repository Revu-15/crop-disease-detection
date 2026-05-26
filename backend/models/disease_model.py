import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout
from tensorflow.keras.optimizers import Adam

class DiseaseModel:
    """Wrapper for disease detection model"""
    
    def __init__(self, input_shape=(224, 224, 3), num_classes=10):
        """Initialize model architecture"""
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = self.build_model()
    
    def build_model(self):
        """Build CNN model architecture"""
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=self.input_shape),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(64, activation='relu'),
            Dropout(0.3),
            Dense(self.num_classes, activation='softmax')
        ])
        return model
    
    def compile(self, learning_rate=0.001):
        """Compile model"""
        optimizer = Adam(learning_rate=learning_rate)
        self.model.compile(
            optimizer=optimizer,
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
    
    def summary(self):
        """Print model summary"""
        return self.model.summary()
    
    def save(self, filepath):
        """Save model to file"""
        self.model.save(filepath)
        print(f"Model saved to {filepath}")
    
    def load(self, filepath):
        """Load model from file"""
        from tensorflow.keras.models import load_model
        self.model = load_model(filepath)
        print(f"Model loaded from {filepath}")
