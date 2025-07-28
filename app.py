import os
import time
import logging
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import urllib.request
from PIL import Image
import tempfile

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Azure Custom Vision configuration
# prediction_endpoint = os.getenv('PredictionEndpoint')
# prediction_key = os.getenv('PredictionKey')
# project_id = os.getenv('ProjectID')
# model_name = os.getenv('ModelName')
prediction_endpoint="https://customvision53325347-prediction.cognitiveservices.azure.com/"
prediction_key="DBOVSjrKNO0V9VMWVPf2Gr8oZqYWH7hTr5MP3GKWlb6HcC8YHxevJQQJ99BGACqBBLyXJ3w3AAAIACOGMbSH"
project_id="8de15e95-469d-4906-9ad3-cb82f64f1b64"
model_name="Iteration1"


def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_prediction_client():
    """Initialize and return Azure Custom Vision prediction client."""
    try:
        credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
        return CustomVisionPredictionClient(endpoint=prediction_endpoint, credentials=credentials)
    except Exception as e:
        logging.error(f"Failed to initialize prediction client: {e}")
        return None

def classify_image_data(image_data):
    """Classify image data using Azure Custom Vision API."""
    try:
        prediction_client = get_prediction_client()
        if not prediction_client:
            return None, "Failed to initialize Azure Custom Vision client"
        
        results = prediction_client.classify_image(project_id, model_name, image_data)
        
        # Filter predictions with probability > 50%
        predictions = []
        for prediction in results.predictions:
            if prediction.probability > 0.5:
                predictions.append({
                    'tag_name': prediction.tag_name,
                    'probability': prediction.probability
                })
        
        return predictions, None
    except Exception as e:
        logging.error(f"Classification error: {e}")
        return None, str(e)

def validate_image(file_path):
    """Validate that the file is a valid image."""
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and classification."""
    try:
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload an image file.', 'error')
            return redirect(url_for('index'))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Validate image
        if not validate_image(file_path):
            os.remove(file_path)
            flash('Invalid image file', 'error')
            return redirect(url_for('index'))
        
        # Read image data for classification
        with open(file_path, "rb") as image_file:
            image_data = image_file.read()
        
        # Classify image
        predictions, error = classify_image_data(image_data)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        if error:
            flash(f'Classification error: {error}', 'error')
            return redirect(url_for('index'))
        
        if not predictions:
            flash('No confident predictions found (all predictions below 50%)', 'warning')
            return redirect(url_for('index'))
        
        # Sort predictions by confidence
        predictions.sort(key=lambda x: x['probability'], reverse=True)
        
        return render_template('index.html', 
                             predictions=predictions, 
                             image_source='uploaded file',
                             filename=filename)
    
    except Exception as e:
        logging.error(f"Upload error: {e}")
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/classify_url', methods=['POST'])
def classify_url():
    """Handle URL-based image classification."""
    try:
        image_url = request.form.get('image_url', '').strip()
        
        if not image_url:
            flash('Please enter a valid image URL', 'error')
            return redirect(url_for('index'))
        
        # Download image from URL
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            try:
                urllib.request.urlretrieve(image_url, temp_file.name)
                
                # Validate image
                if not validate_image(temp_file.name):
                    flash('Invalid image URL or unsupported image format', 'error')
                    return redirect(url_for('index'))
                
                # Read image data for classification
                with open(temp_file.name, "rb") as image_file:
                    image_data = image_file.read()
                
            except Exception as e:
                flash(f'Failed to download image from URL: {str(e)}', 'error')
                return redirect(url_for('index'))
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file.name):
                    os.remove(temp_file.name)
        
        # Classify image
        predictions, error = classify_image_data(image_data)
        
        if error:
            flash(f'Classification error: {error}', 'error')
            return redirect(url_for('index'))
        
        if not predictions:
            flash('No confident predictions found (all predictions below 50%)', 'warning')
            return redirect(url_for('index'))
        
        # Sort predictions by confidence
        predictions.sort(key=lambda x: x['probability'], reverse=True)
        
        return render_template('index.html', 
                             predictions=predictions, 
                             image_source='URL',
                             image_url=image_url)
    
    except Exception as e:
        logging.error(f"URL classification error: {e}")
        flash(f'An error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    flash("File is too large. Maximum size is 16MB.", 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
