# 🏛️ Monument Classification Web App

## Description
The Monument Classification Web App is an AI-powered application that identifies monuments from images using Azure Custom Vision AI. Users can upload an image or provide an image URL, and the app predicts the monument name along with confidence scores.
Built with Flask as the backend and integrated with Azure Custom Vision, the app provides an interactive and user-friendly way to explore machine learning-based image classification. This project demonstrates the use of cloud-based AI services for real-world applications such as cultural heritage recognition and tourism technology.

---

##  Features
-  Upload images or classify images directly from a URL
-  Uses Azure Custom Vision for monument recognition
-  Filters predictions with confidence > 50%
-  Automatic file cleanup after processing
-  Easy deployment on cloud platforms (e.g., Azure App Service, Replit, etc.)

---

##  Tech Stack
- **Python 3.11+**
- **Flask** (for the web interface)
- **Azure Custom Vision Prediction API**
- **Pillow** (for image validation)
- **Gunicorn** (for production deployment)

---

##  Project Structure
```
├── app.py                     # Flask web application
├── test-classifier_*.py       # CLI script to test Azure Custom Vision predictions
├── templates/
│   └── index.html             # Web interface template
├── uploads/                   # Temporary uploaded images
├── pyproject.toml             # Dependencies
├── uv.lock                    # Dependency lock file
└── .replit                    # Configuration for Replit deployment
```

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Joshua-Fernando/Monument-Classifier
cd Monument-Classifier
```

### 2. Install Dependencies
Using **pip**:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
or using **uv**:
```bash
uv sync
```

---

## Azure Custom Vision Setup
1. Create a **Custom Vision** project in the Azure portal.  
2. Train and publish your model.  
3. Get the following credentials:
   - **Prediction Endpoint**
   - **Prediction Key**
   - **Project ID**
   - **Model Name**
4. Add these to your environment variables:
   ```bash
   export PredictionEndpoint="https://<your-endpoint>.cognitiveservices.azure.com/"
   export PredictionKey="your-prediction-key"
   export ProjectID="your-project-id"
   export ModelName="your-model-name"
   ```

---

## Running the Web App
```bash
python app.py
```
Then open your browser and navigate to:
```
http://localhost:5000
```

---

## Running the CLI Test Script
The script `test-classifier_*.py` allows testing classification directly from the terminal:
```bash
python test-classifier_1751276125879.py
```
- It processes images from the `test-images/` folder.
- You can also provide an image URL for classification.

---

## Deployment
You can deploy this project to:
- **Azure App Service**
- **Replit**
- **Heroku**
- **Any cloud hosting that supports Flask**

---

## License
This project is licensed under the **Apache-2.0 license**.

---

### 👨‍💻 Author
Developed by **Joshua Fernando**  
Feel free to contribute or open issues!



