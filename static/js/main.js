document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const API_URL = window.location.origin;
    const fileInput = document.getElementById('eegFile');
    const file = fileInput.files[0];
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const resultAlert = document.getElementById('resultAlert');
    const resultDetails = document.getElementById('resultDetails'); // Add this to your HTML

    if (!file) {
        showAlert('Please select a file', 'warning');
        return;
    }

    const formData = new FormData();
    formData.append('file', file, file.name);

    try {
        loading.style.display = 'block';
        results.style.display = 'none';
        clearResults(); // Clear previous results

        const response = await fetch(`${API_URL}/analyze`, {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        });

        const data = await response.json();
        console.log('Server response:', data);

        loading.style.display = 'none';
        
        if (!response.ok) {
            handleErrorResponse(data, response.status);
            return;
        }

        if (data.status === 'success') {
            displayDetailedResults(data);
        } else {
            showAlert(data.message || 'Unknown error occurred', 'danger');
        }
    } catch (error) {
        loading.style.display = 'none';
        showAlert(`Network Error: ${error.message}`, 'danger');
        console.error('Error:', error);
    }
});

// Helper functions
function showAlert(message, type) {
    const resultAlert = document.getElementById('resultAlert');
    resultAlert.className = `alert alert-${type}`;
    resultAlert.innerHTML = message;
    document.getElementById('results').style.display = 'block';
}

function clearResults() {
    document.getElementById('resultDetails').innerHTML = '';
}

function handleErrorResponse(data, status) {
    let message = 'Error processing file';
    if (status === 503) {
        message = 'Model is still loading. Please try again in a few moments.';
    } else if (data.detail) {
        message = typeof data.detail === 'object' 
            ? data.detail.error || JSON.stringify(data.detail)
            : data.detail;
    }
    showAlert(message, status === 503 ? 'warning' : 'danger');
}

function displayDetailedResults(data) {
    const resultDetails = document.getElementById('resultDetails');
    
    // Basic result
    showAlert(`Analysis Complete: ${data.message}`, 'success');
    
    // Detailed visualization
    resultDetails.innerHTML = `
        <div class="mt-4">
            <h5>Detailed Analysis</h5>
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">Stress Level</div>
                        <div class="card-body">
                            <h2 class="display-4 text-${getStressColor(data.result.stress_level)}">
                                ${data.result.stress_level}
                            </h2>
                            <p>Confidence: ${data.result.confidence}%</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">Brain Wave Metrics</div>
                        <div class="card-body">
                            <ul class="list-group">
                                ${Object.entries(data.result.wave_metrics).map(([wave, value]) => `
                                    <li class="list-group-item d-flex justify-content-between align-items-center">
                                        ${wave}
                                        <span class="badge bg-primary rounded-pill">${value}</span>
                                    </li>
                                `).join('')}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            ${data.result.recommendations ? `
            <div class="card mt-3">
                <div class="card-header">Recommendations</div>
                <div class="card-body">
                    <ul>
                        ${data.result.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                    </ul>
                </div>
            </div>
            ` : ''}
        </div>
    `;
}

function getStressColor(level) {
    const levels = {
        'low': 'success',
        'normal': 'info',
        'moderate': 'warning',
        'high': 'danger'
    };
    return levels[level.toLowerCase()] || 'primary';
}