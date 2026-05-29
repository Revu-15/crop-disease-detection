import os
import json
from datetime import datetime
from tensorflow.keras.models import load_model
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import numpy as np

class ModelEvaluator:
    """Model evaluation utilities"""
    
    @staticmethod
    def evaluate_model(model, X_test, y_test):
        """Evaluate model on test data"""
        y_pred = model.predict(X_test)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_test_classes = np.argmax(y_test, axis=1)
        
        metrics = {
            'accuracy': accuracy_score(y_test_classes, y_pred_classes),
            'precision': precision_score(y_test_classes, y_pred_classes, average='weighted'),
            'recall': recall_score(y_test_classes, y_pred_classes, average='weighted'),
            'f1': f1_score(y_test_classes, y_pred_classes, average='weighted'),
            'confusion_matrix': confusion_matrix(y_test_classes, y_pred_classes).tolist()
        }
        
        return metrics
    
    @staticmethod
    def print_metrics(metrics):
        """Print evaluation metrics"""
        print("\n" + "="*50)
        print("MODEL EVALUATION RESULTS")
        print("="*50)
        print(f"Accuracy:  {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall:    {metrics['recall']:.4f}")
        print(f"F1-Score:  {metrics['f1']:.4f}")
        print("="*50 + "\n")
    
    @staticmethod
    def save_report(metrics, filepath):
        """Save evaluation report to file"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Report saved to {filepath}")
    
    @staticmethod
    def evaluate_per_class(model, X_test, y_test, class_names):
        """Evaluate metrics per class"""
        y_pred = model.predict(X_test)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_test_classes = np.argmax(y_test, axis=1)
        
        per_class_metrics = {}
        
        for i, class_name in enumerate(class_names):
            class_mask = y_test_classes == i
            if class_mask.sum() > 0:
                class_acc = accuracy_score(y_test_classes[class_mask], y_pred_classes[class_mask])
                per_class_metrics[class_name] = {
                    'accuracy': class_acc,
                    'samples': int(class_mask.sum())
                }
        
        return per_class_metrics
    
    @staticmethod
    def plot_confusion_matrix(confusion_mat, class_names, save_path=None):
        """Plot confusion matrix"""
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns
            
            plt.figure(figsize=(12, 10))
            sns.heatmap(confusion_mat, annot=True, fmt='d', cmap='Blues',
                       xticklabels=class_names, yticklabels=class_names)
            plt.title('Confusion Matrix')
            plt.ylabel('True Label')
            plt.xlabel('Predicted Label')
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                print(f"Confusion matrix saved to {save_path}")
            
            plt.show()
        except ImportError:
            print("Matplotlib not installed. Skipping plot.")
