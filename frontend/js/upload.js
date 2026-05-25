// Upload functionality

const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const previewSection = document.getElementById('previewSection');
const analyzeBtn = document.getElementById('analyzeBtn');

let selectedFile = null;

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

imageInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

function handleFileSelect(file) {
    // Validate file
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
    const maxSize = 16 * 1024 * 1024; // 16MB
    
    if (!allowedTypes.includes(file.type)) {
        showError('Invalid file type. Please upload JPG, PNG, or GIF.');
        return;
    }
    
    if (file.size > maxSize) {
        showError('File size exceeds 16MB limit.');
        return;
    }
    
    selectedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('previewImg').src = e.target.result;
        document.getElementById('fileName').textContent = file.name;
        previewSection.style.display = 'block';
        uploadArea.style.display = 'none';
    };
    reader.readAsDataURL(file);
}

function resetUpload() {
    selectedFile = null;
    imageInput.value = '';
    previewSection.style.display = 'none';
    uploadArea.style.display = 'block';
}

analyzeBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        showError('Please select an image first.');
        return;
    }
    
    const formData = new FormData();
    formData.append('image', selectedFile);
    
    try {
        document.getElementById('loading').style.display = 'block';
        analyzeBtn.disabled = true;
        
        const response = await fetch('/api/predict', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Prediction failed');
        }
        
        const result = await response.json();
        
        // Redirect to result page
        const params = new URLSearchParams({
            id: result.prediction.upload_id,
            image: result.prediction.image_path,
            disease: result.prediction.disease_name,
            confidence: result.prediction.confidence
        });
        
        window.location.href = `/result?${params}`;
        
    } catch (error) {
        showError('Error: ' + error.message);
        console.error('Error:', error);
        document.getElementById('loading').style.display = 'none';
        analyzeBtn.disabled = false;
    }
});

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}
