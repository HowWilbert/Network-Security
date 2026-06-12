# Network Security — ML-Based Threat Detection Pipeline

A production-ready, end-to-end Machine Learning pipeline for **network intrusion and threat detection**, built with modular components for data ingestion, validation, transformation, model training, and Dockerized deployment.

---

## Overview

This project implements a full MLOps pipeline to detect malicious network activity using supervised machine learning. The pipeline is designed with clean separation of concerns — each stage (ingestion → validation → transformation → training) is independently configurable and logged, making it easy to extend or swap components.

---

## Tech Stack

| Category | Tools |
|---|---|
| Language | Python |
| ML & Data | Scikit-learn, Pandas, NumPy |
| Pipeline | Custom modular pipeline (config-driven) |
| Logging | Custom logger module |
| Containerization | Docker |
| Data Storage | MongoDB (push_data.py) |
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
└── Readme.md
```

---

## Pipeline Stages

### 1. Data Ingestion
Pulls raw network traffic data and prepares train/test splits based on `DataIngestionConfig`.

### 2. Data Validation
Validates ingested data against a predefined schema (column names, data types, null checks) to ensure data integrity before transformation.

### 3. Data Transformation
Applies preprocessing — handles missing values, encodes categorical features, and scales numerical features — producing transformed arrays ready for model training.

### 4. Model Training
Trains a classification model on transformed data, evaluates performance, and serializes the best model artifact.

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

The project uses network traffic data stored under `Network_data/`. Features represent packet-level attributes commonly used in intrusion detection (e.g., duration, protocol type, flag, byte counts).

Data schema is defined in `data_schema/` and used by the validation component to enforce integrity checks.

---

## Key Design Decisions

- **Config-driven pipeline** — all paths, thresholds, and parameters are centralized in `config_entity.py`, making the pipeline reproducible and easy to tune.
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