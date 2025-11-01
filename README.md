# Network Security project for Phising Data


This project, Building Network System Security, is a modular Python-based ML system designed to detect phishing or malicious network activity using supervised learning techniques.
It is architected with high scalability, modularity, and production readiness in mind — similar to real-world MLOps pipelines at enterprise level.

The system handles:

✅ Automated Data Ingestion

✅ Data Validation and Transformation

✅ Model Training and Artifact Management

✅ Cloud Synchronization via AWS S3

✅ FastAPI-based deployment for real-time predictions


                ┌────────────────────────┐
                │   Data Ingestion        │
                │  (Collect Raw Data)     │
                └──────────┬──────────────┘
                           │
                ┌──────────▼──────────────┐
                │   Data Validation       │
                │ (Schema & Integrity)    │
                └──────────┬──────────────┘
                           │
                ┌──────────▼──────────────┐
                │  Data Transformation    │
                │ (Clean & Encode)        │
                └──────────┬──────────────┘
                           │
                ┌──────────▼──────────────┐
                │    Model Trainer        │
                │ (Train + Evaluate)      │
                └──────────┬──────────────┘
                           │
                ┌──────────▼──────────────┐
                │   Model Storage (S3)    │
                │ (Save + Sync Artifacts) │
                └──────────┬──────────────┘
                           │
                ┌──────────▼──────────────┐
                │ FastAPI App Interface   │
                │ (/train & /predict)     │
                └────────────────────────┘


🧱 Prerequisites

Make sure you have the following installed:

Python 3.8+

pip

AWS CLI (configured)

MongoDB (Atlas or Local)

Git


# 1️⃣ Clone the repository
git clone https://github.com/faizan23804/Building-Network-System-Security.git
cd Building-Network-System-Security

# 2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate       # (Windows)
source venv/bin/activate    # (Mac/Linux)

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Configure environment variables
Create a `.env` file with:
MONGODB_URL_KEY="your_mongodb_connection_string"

# 5️⃣ Set up AWS credentials
aws configure
# (Provide your access key, secret key, and region)



🚀 Running the Project
🔹 1. Train the Model

Start the FastAPI server:
python app.py

Then open in your browser:
👉 http://127.0.0.1:8000/docs

Click on /train → Try it out → Execute

This will:

Trigger the Train_Test_Pipeline

Run all modules (ingestion → validation → transformation → model training)

Save trained models and push artifacts to AWS S3

🔹 2. Make Predictions

Still in Swagger UI:

Go to /predict

Upload your CSV file (with input features)

The endpoint will:

Load preprocessor.pkl and model.pkl

Predict the target variable

Return an HTML table view of predictions

The predictions are also saved at:

prediction_output/output.csv

💡 Tech Stack
Category	Tools / Libraries
Language	Python 3.8+
Framework	FastAPI
ML/DS	scikit-learn, pandas, numpy
Cloud	AWS S3
Database	MongoDB
Environment	dotenv
Version Control	Git, GitHub
Deployment	Uvicorn
