# Network Security — ML-Based Threat Detection Pipeline
 
A production-ready, end-to-end Machine Learning pipeline for **network intrusion and threat detection**, built with modular components for data ingestion, validation, transformation, model training, and Dockerized deployment.
 
---
 
## Overview
 
This project implements a full MLOps pipeline to detect malicious network activity using supervised machine learning. The pipeline is designed with clean separation of concerns — each stage (ingestion → validation → transformation → training) is independently configurable and logged, making it easy to extend or swap components.
 
---
 
## Model Performance
 
Results from the latest training run (`2026-06-11`):
 
| Metric | Train | Test |
|---|---|---|
| **F1 Score** | 0.9919 | 0.9694 |
| **Precision** | 0.9886 | 0.9662 |
| **Recall** | 0.9954 | 0.9727 |
 
> The model generalizes well with minimal train-test gap, indicating low overfitting. Test F1 of **0.9694** reflects strong real-world threat detection capability.
 
---
 
## Tech Stack
 
| Category | Tools |
|---|---|
| Language | Python |
| ML & Data | Scikit-learn, Pandas, NumPy |
| Imputation | KNNImputer (k=3, uniform weights) |
| Pipeline | Custom modular pipeline (config-driven) |
| Logging | Custom logger module |
| Containerization | Docker |
| Data Storage | MongoDB (`push_data.py`) |
| Version Control | Git, GitHub |
 
---
 
## Project Structure
 
```
Network-Security/
│
├── networksequrity/               # Core package
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   ├── entity/
│   │   └── config_entity.py       # Pipeline config dataclasses
│   ├── logging/
│   │   └── logger.py
│   └── exception/
│       └── exception.py
│
├── Network_data/                  # Raw network traffic data
├── data_schema/                   # Schema definitions for validation
├── main.py                        # Pipeline entry point
├── push_data.py                   # Data ingestion to MongoDB
├── DockerFile                     # Docker container config
├── requirements.txt
├── setup.py
└── README.md
```
 
---
 
## Pipeline Stages
 
### 1. Data Ingestion
Pulls raw network traffic data, performs train/test split, and exports file paths to the artifact store. Completed in ~3 seconds.
 
### 2. Data Validation
Validates ingested data against a predefined schema:
- Checks for required **31 columns** (train and test sets)
- Confirms all **31 columns are numerical** — no unexpected categorical features
- Schema defined in `data_schema/` for reproducibility
### 3. Data Transformation
Applies preprocessing using a `KNNImputer` (k=3, uniform weights) to handle missing values in network traffic data. Preprocessor object is serialized to the artifact store for reuse during inference.
 
### 4. Model Training
Trains a classification model on the transformed 31-feature dataset. The trained model is saved at:
```
Artifacts/<timestamp>/model_trainer/trained_model/model.pkl
```
Training completed in approximately **3 minutes 44 seconds**.
 
---
 
## Getting Started
 
### Prerequisites
- Python 3.8+
- Docker (optional, for containerized run)
- MongoDB (for `push_data.py`)
### Installation
 
```bash
git clone https://github.com/HowWilbert/Network-Security.git
cd Network-Security
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
 
### Run the Training Pipeline
 
```bash
python main.py
```
 
This triggers the full pipeline: Data Ingestion → Data Validation → Data Transformation → Model Training. Logs are printed at each stage.
 
### Push Data to MongoDB
 
```bash
python push_data.py
```
 
---
 
## Docker
 
### Build
 
```bash
docker build -t network-security .
```
 
### Run
 
```bash
docker run network-security
```
 
---
 
## Dataset
 
The project uses network traffic data stored under `Network_data/`. The dataset contains **31 numerical features** representing packet-level and flow-level attributes used for binary/multi-class intrusion detection.
 
Schema is defined in `data_schema/` and enforced during the validation stage.
 
---
 
## Key Design Decisions
 
- **Config-driven pipeline** — all paths, thresholds, and parameters are centralized in `config_entity.py`, making the pipeline reproducible and easy to tune.
- **KNN Imputation** — missing values in network traffic data are imputed using k=3 nearest neighbors, preserving feature relationships better than mean/median imputation.
- **Artifact versioning** — all outputs (preprocessor, model) are saved under timestamped directories (`Artifacts/<timestamp>/...`) for full run traceability.
- **Custom exception handling** — `NetworkSecurityException` wraps all errors with traceback context for clean debugging.
- **Structured logging** — every pipeline stage logs entry/exit, enabling easy monitoring in production.
---
 
## Future Improvements
 
- FastAPI inference endpoint for real-time threat scoring
- MLflow experiment tracking integration
- CI/CD pipeline with GitHub Actions
- Automated retraining on data drift detection
---
 
## Author
 
**Ansh Bire**
- GitHub: [HowWilbert](https://github.com/HowWilbert)
- LinkedIn: [anshbire](https://www.linkedin.com/in/anshbire)
---
 
## License
 
This project is open-source and available under the MIT License.