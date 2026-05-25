// API helper functions

const API_BASE_URL = '/api';

class API {
    static async predict(file) {
        const formData = new FormData();
        formData.append('image', file);
        
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Prediction failed');
        }
        
        return response.json();
    }
    
    static async getHistory(limit = 20, page = 1) {
        const response = await fetch(`${API_BASE_URL}/history?limit=${limit}&page=${page}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch history');
        }
        
        return response.json();
    }
    
    static async getHistoryItem(id) {
        const response = await fetch(`${API_BASE_URL}/history/${id}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch history item');
        }
        
        return response.json();
    }
    
    static async deleteHistoryItem(id) {
        const response = await fetch(`${API_BASE_URL}/history/delete/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Failed to delete history item');
        }
        
        return response.json();
    }
    
    static async getAllDiseases() {
        const response = await fetch(`${API_BASE_URL}/diseases`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch diseases');
        }
        
        return response.json();
    }
    
    static async getDiseaseDetails(diseaseName) {
        const response = await fetch(`${API_BASE_URL}/disease/${encodeURIComponent(diseaseName)}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch disease details');
        }
        
        return response.json();
    }
    
    static async healthCheck() {
        const response = await fetch(`${API_BASE_URL}/health`);
        
        if (!response.ok) {
            throw new Error('API is not available');
        }
        
        return response.json();
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API;
}
