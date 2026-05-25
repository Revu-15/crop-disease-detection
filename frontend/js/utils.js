// Utility functions

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function getConfidenceColor(confidence) {
    if (confidence >= 0.9) return '#27ae60'; // Green
    if (confidence >= 0.7) return '#f39c12'; // Orange
    return '#e74c3c'; // Red
}

function getSeverityColor(severity) {
    switch(severity.toLowerCase()) {
        case 'high':
            return '#e74c3c';
        case 'medium':
            return '#f39c12';
        case 'low':
            return '#27ae60';
        default:
            return '#95a5a6';
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    const style = document.createElement('style');
    if (!document.querySelector('style[data-notification]')) {
        style.setAttribute('data-notification', 'true');
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 1rem 1.5rem;
                border-radius: 5px;
                color: white;
                font-weight: 500;
                z-index: 1000;
                animation: slideIn 0.3s ease-out;
            }
            .notification-info {
                background-color: #3498db;
            }
            .notification-success {
                background-color: #27ae60;
            }
            .notification-error {
                background-color: #e74c3c;
            }
            .notification-warning {
                background-color: #f39c12;
            }
            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideIn 0.3s ease-out reverse';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function toggleLoadingState(element, isLoading) {
    if (isLoading) {
        element.disabled = true;
        element.style.opacity = '0.6';
        element.innerHTML = '<span class="spinner"></span> Loading...';
    } else {
        element.disabled = false;
        element.style.opacity = '1';
        element.innerHTML = 'Analyze Image';
    }
}
