import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.model import ContrastiveModel, extract_features
from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from starlette.middleware.sessions import SessionMiddleware
import torch
import numpy as np
from pathlib import Path
import os
import mne
import tempfile
from app.model import ContrastiveModel, extract_features
from joblib import load

app = FastAPI(title="EEG Stress Detection")

# Add session middleware AFTER app is created
app.add_middleware(SessionMiddleware, secret_key="your-super-secret-key-change-this-in-production")

# Get the absolute path to the project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check if CUDA is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Global variables
model = None
model_loaded = False
model_loading = False
input_dim = 155  # Number of features (31 channels * 5 features per channel)

def load_model():
    global model, model_loaded, model_loading
    try:
        if model_loaded:
            return True
        if model_loading:
            return False
        
        model_loading = True
        model_path = BASE_DIR / "best_model.joblib"
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found at {model_path}")
            
        model = ContrastiveModel.load_model(str(model_path))
        model.to(device)
        model.eval()
        model_loaded = True
        model_loading = False
        return True
    except Exception as e:
        model_loading = False
        return False

@app.on_event("startup")
async def startup_event():
    if not load_model():
        print("WARNING: Failed to load model during startup!")

# Routes (login/logout/home remain the same as in your original code)

def process_edf_file(file_path):
    """Process a single EDF file and extract features"""
    try:
        # Read EEG file using MNE
        raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
        
        # Basic preprocessing
        raw.filter(1, 40, fir_design='firwin')
        
        # Extract features
        features = extract_features(raw)
        
        return features
    except Exception as e:
        raise ValueError(f"Error processing EEG file: {str(e)}")

def get_stress_level(prediction, confidence):
    """Convert prediction to stress level with confidence"""
    if prediction == 1:  # High stress
        return {
            'level': 'high',
            'label': 'High Stress',
            'confidence': confidence,
            'recommendations': [
                'Take a 15-minute break',
                'Practice deep breathing for 5 minutes',
                'Consider a short walk outside'
            ]
    }
    else:  # Low stress
        return {
            'level': 'low',
            'label': 'Low Stress',
            'confidence': confidence,
            'recommendations': [
                'Maintain your current routine',
                'Stay hydrated',
                'Consider mindfulness exercises'
            ]
    }

def get_wave_metrics(raw):
    """Extract wave metrics from EEG data"""
    # Get power in different frequency bands
    psd, freqs = mne.time_frequency.psd_welch(raw, fmin=1, fmax=40)
    
    # Calculate relative power in different bands
    def band_power(fmin, fmax):
        band = np.logical_and(freqs >= fmin, freqs <= fmax)
        return psd[:, band].mean(axis=1).mean()
    
    return {
        'alpha': band_power(8, 13),
        'beta': band_power(13, 30),
        'theta': band_power(4, 8),
        'gamma': band_power(30, 40),
        'delta': band_power(1, 4)
    }

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        if not model_loaded:
            raise HTTPException(
                status_code=503,
                detail="Model is still loading. Please try again in a few moments."
            )

        if not file or not file.filename:
            raise HTTPException(status_code=400, detail="No file uploaded")
        
        if not file.filename.endswith('.edf'):
            raise HTTPException(status_code=400, detail="Invalid file format. Please upload an EDF file.")

        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.edf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name

        try:
            # Process the file
            raw = mne.io.read_raw_edf(temp_file_path, preload=True, verbose=False)
            raw.filter(1, 40, fir_design='firwin')
            
            # Extract features and wave metrics
            features = extract_features(raw)
            wave_metrics = get_wave_metrics(raw)
            
            # Prepare model input
            features = features.reshape(-1)[:input_dim]
            if len(features) < input_dim:
                features = np.pad(features, (0, input_dim - len(features)))

            # Make prediction
            input_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
            with torch.no_grad():
                output = model(input_tensor)
                probabilities = torch.softmax(output, dim=1).numpy()[0]
                prediction = torch.argmax(output, dim=1).item()
                confidence = round(max(probabilities) * 100, 1)
            
            # Format results
            stress_info = get_stress_level(prediction, confidence)
            
            return {
                'status': 'success',
                'stress_level': stress_info['level'],
                'stress_label': stress_info['label'],
                'confidence': confidence,
                'wave_metrics': wave_metrics,
                'recommendations': stress_info['recommendations'],
                'message': f"Analysis complete: {stress_info['label']} detected with {confidence}% confidence"
            }

        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass

    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "detail": str(e),
                "message": "Failed to process EEG file"
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)