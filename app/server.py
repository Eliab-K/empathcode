from flask import Flask, request, jsonify
import mne
import tempfile
import os
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('EEG-API')

@app.route('/analyze', methods=['POST'])
def analyze_eeg():
    logger.info(f"\n\nNew request received at {datetime.utcnow()}")
    
    if 'eeg_file' not in request.files:
        logger.error("No file part in request")
        return jsonify({"error": "No file provided"}), 400

    file = request.files['eeg_file']
    if file.filename == '':
        logger.error("Empty filename")
        return jsonify({"error": "No selected file"}), 400

    try:
        # Save to temporary file
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, file.filename)
        file.save(temp_path)
        logger.info(f"Saved temporary file to {temp_path}")

        # Process EEG
        logger.info("Attempting to read EDF file...")
        raw = mne.io.read_raw_edf(temp_path, preload=True)
        logger.info("Successfully loaded EDF file")
        
        # Your existing analysis code here
        results = {
            "status": "success",
            "message": "Processing completed",
            "data": {}  # Add your actual results
        }
        
        return jsonify(results)

    except Exception as e:
        logger.error(f"Processing failed: {str(e)}", exc_info=True)
        return jsonify({
            "error": "EEG processing failed",
            "details": str(e)
        }), 500

    finally:
        # Clean up
        if 'temp_path' in locals() and os.path.exists(temp_path):
            os.remove(temp_path)
            os.rmdir(temp_dir)
            logger.info("Cleaned up temporary files")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)