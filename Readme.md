# 🛡️ Network Security — ML-Based Phishing & Threat Detection System

A production-grade, end-to-end Machine Learning system for **network intrusion and phishing detection**, featuring a modular ML pipeline, FastAPI inference server, MLflow experiment tracking, and a fully automated CI/CD pipeline deploying to AWS via Docker and GitHub Actions.

---

## 📊 Model Performance

Results from the latest training run:

| Metric | Train | Test |
|---|---|---|
| **F1 Score** | 0.9919 | 0.9694 |
| **Precision** | 0.9886 | 0.9662 |
| **Recall** | 0.9954 | 0.9727 |

> The model generalizes exceptionally well with a train-test F1 gap of only **~0.02**, indicating minimal overfitting. A test F1 of **0.9694** demonstrates strong real-world threat detection capability.

### Models Evaluated

The pipeline performs hyperparameter-tuned model selection across 5 classifiers:

| Model | Hyperparameters Tuned |
|---|---|
| Random Forest | `n_estimators`: [8, 16, 32, 128, 256] |
| Decision Tree | `criterion`: [gini, entropy, log_loss] |
| Gradient Boosting | `learning_rate`, `subsample`, `n_estimators` |
| Logistic Regression | Default |
| AdaBoost | `learning_rate`, `n_estimators` |

The best model is automatically selected based on the highest evaluation score and tracked via **MLflow + DagsHub**.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        GitHub (main branch)                        │
│                         Push triggers CI/CD                        │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │   GitHub Actions CI   │
                    │  (Lint + Unit Tests)  │
                    └───────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │  Continuous Delivery  │
                    │  Build Docker Image   │
                    │  Push to AWS ECR      │
                    └───────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │ Continuous Deployment │
                    │  Self-Hosted Runner   │
                    │  (EC2 Instance)       │
                    │  Pull & Run Container │
                    └───────────┬───────────┘
                                │
              ┌─────────────────▼─────────────────┐
              │         FastAPI Server             │
              │  http://<EC2-IP>:8000/docs         │
              │                                    │
              │  GET  /        → Redirect to docs  │
              │  GET  /train   → Run ML Pipeline   │
              │  POST /predict → Upload CSV → Get  │
              │                  predictions       │
              └─────────────────┬─────────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          │                     │                     │
  ┌───────▼───────┐   ┌────────▼────────┐   ┌────────▼────────┐
  │   MongoDB     │   │   AWS S3        │   │  DagsHub/MLflow │
  │  (Raw Data)   │   │  (Artifacts &   │   │  (Experiment    │
  │               │   │   Final Model)  │   │   Tracking)     │
  └───────────────┘   └─────────────────┘   └─────────────────┘
```

---

## 🔧 Tech Stack

| Category | Tools |
|---|---|
| **Language** | Python 3.12 |
| **ML & Data** | Scikit-learn, Pandas, NumPy |
| **Imputation** | KNNImputer (k=3, uniform weights) |
| **API Framework** | FastAPI + Uvicorn |
| **Experiment Tracking** | MLflow + DagsHub |
| **Data Storage** | MongoDB Atlas |
| **Cloud Storage** | AWS S3 |
| **Container Registry** | AWS ECR |
| **Compute** | AWS EC2 (Self-Hosted Runner) |
| **Containerization** | Docker (Python 3.12 slim-bookworm) |
| **CI/CD** | GitHub Actions (3-stage pipeline) |
| **Version Control** | Git, GitHub |

---

## 📁 Project Structure

```
Network-Security/
│
├── .github/
│   └── workflows/
│       └── main.yml                    # CI/CD pipeline (3 jobs)
│
├── networksequrity/                    # Core ML package
│   ├── components/
│   │   ├── data_ingestion.py           # MongoDB → Train/Test split
│   │   ├── data_validation.py          # Schema validation + drift report
│   │   ├── data_transformation.py      # KNN imputation + preprocessing
│   │   └── model_trainer.py            # Model selection + MLflow tracking
│   ├── cloud/
│   │   └── s3_syncer.py                # AWS S3 upload/download
│   ├── constant/
│   │   └── training_pipeline/
│   │       └── __init__.py             # All pipeline constants & thresholds
│   ├── entity/
│   │   ├── config_entity.py            # Pipeline config dataclasses
│   │   └── artifact_entity.py          # Artifact dataclasses
│   ├── exception/
│   │   └── exception.py                # Custom exception with traceback
│   ├── logging/
│   │   └── logger.py                   # Structured logging
│   ├── pipeline/
│   │   └── training_pipeline.py        # Orchestrates all pipeline stages
│   └── utils/
│       ├── main_utils/
│       │   └── utils.py                # Save/load objects, evaluate models
│       └── ml_utils/
│           ├── metric/
│           │   └── classification_metric.py
│           └── model/
│               └── estimator.py        # NetworkModel wrapper
│
├── Network_data/                       # Raw phishing dataset
├── data_schema/                        # Schema definitions (YAML)
├── templates/                          # Jinja2 HTML templates for FastAPI
├── prediction_output/                  # CSV prediction results
│
├── app.py                              # FastAPI application entry point
├── main.py                             # Local pipeline runner
├── push_data.py                        # Load CSV data into MongoDB
├── DockerFile                          # Docker container configuration
├── requirements.txt                    # Python dependencies
├── setup.py                            # Package configuration
└── README.md
```

---

## 🔄 ML Pipeline Stages

### 1. Data Ingestion
- Connects to **MongoDB Atlas** and pulls the raw network traffic dataset
- Performs an **80/20 train-test split**
- Exports file paths as `DataIngestionArtifact`

### 2. Data Validation
- Validates ingested data against a predefined YAML schema
- Checks for required **31 numerical columns** in both train and test sets
- Generates a **drift report** comparing train/test distributions
- Flags invalid data and routes it to a separate directory

### 3. Data Transformation
- Applies **KNN Imputation** (k=3, uniform weights) to handle missing values
- Preserves feature relationships better than mean/median imputation
- Serializes the fitted preprocessor (`preprocessor.pkl`) for reuse during inference
- Outputs transformed data as `.npy` arrays

### 4. Model Training
- Trains and evaluates **5 classifiers** with hyperparameter tuning via `GridSearchCV`
- Automatically selects the **best performing model** based on evaluation score
- Tracks all experiments (F1, Precision, Recall) to **MLflow via DagsHub**
- Saves the final model (`model.pkl`) and pushes artifacts to **AWS S3**
- Enforces a minimum expected accuracy threshold of **0.6**
- Rejects models with train-test performance gap exceeding **0.05**

---

## 🌐 API Endpoints

The application exposes a **FastAPI** server with the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Redirects to `/docs` (Swagger UI) |
| `GET` | `/docs` | Interactive API documentation |
| `GET` | `/train` | Triggers the full ML training pipeline |
| `POST` | `/predict` | Upload a CSV file → returns predictions as an HTML table |

### Prediction Flow
1. Upload a CSV file with 30 network traffic features
2. The API loads the trained preprocessor and model from `final_model/`
3. Applies KNN imputation and generates predictions
4. Returns an HTML table with a new `predicted_column` (0 = Safe, 1 = Threat)
5. Saves results to `prediction_output/output.csv`

---

## 🚀 CI/CD Pipeline

The project uses a **3-stage GitHub Actions pipeline** triggered on every push to `main`:

### Stage 1: Continuous Integration (`ubuntu-latest`)
- Checks out code
- Runs linting
- Runs unit tests

### Stage 2: Continuous Delivery (`ubuntu-latest`)
- Configures AWS credentials
- Logs into **Amazon ECR**
- Auto-creates the ECR repository if it doesn't exist
- Builds, tags, and pushes Docker image to ECR

### Stage 3: Continuous Deployment (`self-hosted` EC2 runner)
- Logs into ECR from the EC2 instance
- **Stops** the running container (zero-downtime preparation)
- **Prunes** all unused Docker images (`docker system prune -af`) to prevent disk overflow
- **Pulls** the latest image from ECR
- **Runs** the new container on port `8000`

> **Note:** The pipeline is designed for small EC2 instances (e.g., AWS Free Tier 8GB). The aggressive prune-before-pull strategy ensures the server never runs out of disk space.

---

## 🛠️ Getting Started

### Prerequisites
- Python 3.10+
- Docker
- MongoDB Atlas account (or local MongoDB)
- AWS Account with IAM credentials (for S3, ECR, EC2)

### Local Installation

```bash
git clone https://github.com/HowWilbert/Network-Security.git
cd Network-Security
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
MONGODB_URL_KEY=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/
AWS_ACCESS_KEY_ID=<your-aws-access-key>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-key>
AWS_REGION=us-east-1
```

### Push Data to MongoDB

```bash
python push_data.py
```

### Run the Training Pipeline (Local)

```bash
python main.py
```

This triggers the full pipeline: Data Ingestion → Data Validation → Data Transformation → Model Training.

### Run the FastAPI Server (Local)

```bash
python app.py
```

Then visit: `http://localhost:8000/docs`

---

## 🐳 Docker

### Build

```bash
docker build -t network-security .
```

### Run

```bash
docker run -d -p 8000:8000 \
  -e AWS_ACCESS_KEY_ID=<key> \
  -e AWS_SECRET_ACCESS_KEY=<secret> \
  -e AWS_REGION=us-east-1 \
  network-security
```

Then visit: `http://localhost:8000/docs`

---

## ☁️ AWS Infrastructure

| Service | Purpose |
|---|---|
| **EC2** | Hosts the self-hosted GitHub Actions runner and serves the Docker container |
| **ECR** | Stores versioned Docker images |
| **S3** | Stores pipeline artifacts and trained models (`s3://netwworksecurity-743220303037-us-east-1-an/`) |
| **IAM** | Manages access credentials for ECR, S3, and EC2 |

### EC2 Security Group (Inbound Rules)

| Type | Port | Source |
|---|---|---|
| SSH | 22 | 0.0.0.0/0 |
| HTTP | 80 | 0.0.0.0/0 |
| HTTPS | 443 | 0.0.0.0/0 |
| Custom TCP | 8000 | 0.0.0.0/0 |

---

## 📈 Experiment Tracking

All training experiments are tracked via **MLflow** integrated with **DagsHub**:

- **Metrics logged:** F1 Score, Precision, Recall (for both train and test sets)
- **Models logged:** The best-performing sklearn model is serialized and versioned
- **Dashboard:** [DagsHub Repository](https://dagshub.com/HowWilbert/Network-Security)

---

## 🗄️ Dataset

The project uses a **phishing/network intrusion dataset** with:
- **31 numerical features** representing packet-level and flow-level network attributes
- **Binary target** (`Result`): 1 = Phishing/Malicious, 0 = Legitimate
- Data is stored in MongoDB Atlas (database: `ANSHBIRE`, collection: `NetworkData`)
- Schema enforced via `data_schema/schema.yaml` during validation

---

## 🧠 Key Design Decisions

| Decision | Rationale |
|---|---|
| **Config-driven pipeline** | All paths, thresholds, and parameters are centralized in `config_entity.py` and `training_pipeline/__init__.py`, making the pipeline reproducible and easy to tune |
| **KNN Imputation (k=3)** | Preserves feature relationships in network data better than mean/median imputation |
| **Artifact versioning** | All outputs (preprocessor, model, data) are saved under timestamped directories (`Artifacts/<timestamp>/`) for full run traceability |
| **Lazy DagsHub initialization** | `dagshub.init()` runs only during model training, not at import time — prevents crashes in Docker containers that lack a `.git` directory |
| **Prune-before-pull deployment** | Aggressively cleans Docker images before pulling new ones to prevent disk overflow on small EC2 instances |
| **Custom exception handling** | `NetworkSecurityException` wraps all errors with file name, line number, and traceback for clean debugging |
| **Structured logging** | Every pipeline stage logs entry/exit with timestamps, enabling easy monitoring in production |

---

## 📋 GitHub Secrets Required

To run the CI/CD pipeline, configure these secrets in your GitHub repository (`Settings → Secrets and variables → Actions`):

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
| `AWS_REGION` | AWS region (e.g., `us-east-1`) |
| `ECR_REPOSITORY_NAME` | ECR repository name (e.g., `networkssecurity`) |

---

## 👤 Author

**Ansh Bire**
- GitHub: [HowWilbert](https://github.com/HowWilbert)
- LinkedIn: [anshbire](https://www.linkedin.com/in/anshbire)
- Email: bireansh1@gmail.com

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).