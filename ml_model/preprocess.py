import os
import cv2
import numpy as np
from PIL import Image
from sklearn.preprocessing import StandardScaler

class ImagePreprocessor:
    """Image preprocessing utilities"""
    
    @staticmethod
    def load_image(image_path, target_size=(224, 224)):
        """Load and preprocess image"""
        img = Image.open(image_path).convert('RGB')
        img = img.resize(target_size)
        img_array = np.array(img) / 255.0
        return img_array
    
    @staticmethod
    def augment_image(image, rotation=15, shift=0.1, zoom=0.2):
        """Apply data augmentation to image"""
        from tensorflow.keras.preprocessing.image import ImageDataGenerator
        
        datagen = ImageDataGenerator(
            rotation_range=rotation,
            width_shift_range=shift,
            height_shift_range=shift,
            zoom_range=zoom,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        
        image = np.expand_dims(image, 0)
        augmented = next(datagen.flow(image))
        return augmented[0]
    
    @staticmethod
    def normalize_image(image):
        """Normalize image pixel values"""
        return image / 255.0
    
    @staticmethod
    def apply_histogram_equalization(image):
        """Enhance image contrast using histogram equalization"""
        img_uint8 = (image * 255).astype(np.uint8)
        if len(img_uint8.shape) == 3:
            # Convert to HSV and equalize V channel
            hsv = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2HSV)
            h, s, v = cv2.split(hsv)
            v = cv2.equalizeHist(v)
            hsv = cv2.merge([h, s, v])
            return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB) / 255.0
        else:
            equalized = cv2.equalizeHist(img_uint8)
            return equalized / 255.0
    
    @staticmethod
    def extract_features(image):
        """Extract features from image"""
        # Convert to LAB color space for better disease detection
        img_uint8 = (image * 255).astype(np.uint8)
        lab = cv2.cvtColor(img_uint8, cv2.COLOR_RGB2LAB)
        
        # Calculate color statistics
        l_mean, l_std = cv2.meanStdDev(lab[:, :, 0])
        a_mean, a_std = cv2.meanStdDev(lab[:, :, 1])
        b_mean, b_std = cv2.meanStdDev(lab[:, :, 2])
        
        features = np.array([
            l_mean[0], l_std[0],
            a_mean[0], a_std[0],
            b_mean[0], b_std[0]
        ])
        
        return features
