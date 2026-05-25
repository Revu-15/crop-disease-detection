// Application entry point

document.addEventListener('DOMContentLoaded', function() {
    const url = new URL(window.location.href);
    const uploadId = url.searchParams.get('id');
    const imagePath = url.searchParams.get('image');
    const diseaseName = url.searchParams.get('disease');
    const confidence = url.searchParams.get('confidence');
    
    if (uploadId && diseaseName && confidence) {
        loadResult(uploadId, imagePath, diseaseName, confidence);
    }
});

function loadResult(uploadId, imagePath, diseaseName, confidence) {
    const resultSection = document.getElementById('resultSection');
    const errorSection = document.getElementById('error');
    
    try {
        // Set image
        document.getElementById('resultImg').src = imagePath;
        
        // Fetch disease details
        fetch(`/api/disease/${encodeURIComponent(diseaseName)}`)
            .then(response => response.json())
            .then(data => {
                const diseaseInfo = data.disease_info;
                
                // Set disease name and confidence
                document.getElementById('diseaseName').textContent = diseaseName;
                document.getElementById('confidence').textContent = (confidence * 100).toFixed(2) + '%';
                
                // Set severity badge
                const severityBadge = document.getElementById('severityBadge');
                const severity = diseaseInfo.severity;
                severityBadge.textContent = severity;
                severityBadge.className = 'severity-badge severity-' + severity.toLowerCase();
                
                // Set disease details
                document.getElementById('description').textContent = diseaseInfo.description;
                document.getElementById('symptoms').textContent = diseaseInfo.symptoms;
                document.getElementById('prevention').textContent = diseaseInfo.prevention_tips;
                document.getElementById('treatment').textContent = diseaseInfo.suggested_pesticide;
                document.getElementById('duration').textContent = diseaseInfo.treatment_duration;
                document.getElementById('fertilizer').textContent = diseaseInfo.recommended_fertilizer;
                
                resultSection.style.display = 'block';
            })
            .catch(error => {
                showError('Error loading disease details: ' + error.message);
                console.error('Error:', error);
            });
    } catch (error) {
        showError('Error displaying result: ' + error.message);
        console.error('Error:', error);
    }
}

function showError(message) {
    const errorSection = document.getElementById('error');
    errorSection.textContent = message;
    errorSection.style.display = 'block';
}
