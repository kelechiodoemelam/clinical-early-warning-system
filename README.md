#  Clinical Early Warning System

> A healthcare data integration platform with predictive analytics for patient risk assessment

**Portfolio Project by Kelechi Odoemelam**  
Designed to demonstrate data engineering capabilities for NHS Secure Data Environment roles

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green)](https://flask.palletsprojects.com/)

---

##  Overview

This system demonstrates end-to-end data engineering for healthcare applications, specifically designed to showcase skills relevant to NHS Secure Data Environment (SDE) roles. It integrates patient vital signs data from multiple clinical systems and uses machine learning to predict patient deterioration risk.

### The Challenge

Healthcare organizations face critical challenges:
- **Data Silos**: Clinical data exists in isolated systems (ICU monitors, A&E triage, ward systems)
- **Early Warning**: Manual monitoring can miss early signs of patient deterioration
- **Data Protection**: Handling sensitive patient data requires robust governance
- **Scale**: Systems must handle continuous real-time data from multiple sources

### The Solution

A platform that:
1.  Ingests data from diverse clinical systems
2.  Anonymizes and securely stores patient information
3.  Applies machine learning to predict deterioration risk
4.  Provides real-time dashboards for clinical staff
5.  Maintains comprehensive audit trails for governance

---

##  Key Features

### Data Engineering
- **Multi-Source Integration**: Ingests data from simulated ICU, A&E, and Ward systems
- **Real-time Processing**: Handles continuous vital signs streams
- **Data Validation**: Robust error handling and input validation
- **Scalable Architecture**: RESTful API design suitable for microservices

### Machine Learning
- **Random Forest Classifier**: Proven effective for imbalanced healthcare datasets
- **6 Vital Sign Parameters**: Heart rate, blood pressure, respiratory rate, temperature, oxygen saturation
- **Class Balancing**: Handles low-incidence deterioration events (similar to predictive maintenance)
- **Interpretable Results**: Feature importance scores explain predictions

### Data Protection & Governance
- **Patient Anonymization**: SHA-256 hashing for all patient identifiers
- **Audit Logging**: Complete trail of data access and modifications
- **GDPR Compliance**: Privacy-by-design architecture
- **Source Tracking**: Records which clinical system provided each data point

### User Interface
- **Real-time Dashboard**: Live monitoring of patient risk levels
- **Risk Stratification**: Clear visual indicators (HIGH/MEDIUM/LOW)
- **Auto-refresh**: Updates every 30 seconds
- **System Statistics**: Monitor platform performance and usage

---

##  Architecture
```
┌─────────────────────────────────────────────────────────────┐
│              Clinical Systems Layer                          │
│  (ICU Monitors)  (A&E Triage)  (Ward Vital Signs)          │
└────────────┬────────────┬────────────┬─────────────────────┘
             │            │            │
             └────────────┼────────────┘
                          │
                    ┌─────▼──────┐
                    │  REST API  │
                    │  (Flask)   │
                    └─────┬──────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
   │ Data    │      │ ML      │      │ Audit   │
   │ Storage │      │ Engine  │      │ Logger  │
   │(SQLite) │      │(RF)     │      │         │
   └─────────┘      └─────────┘      └─────────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                    ┌─────▼──────┐
                    │ Dashboard  │
                    │ (Web UI)   │
                    └────────────┘
```

---

##  Technology Stack

**Backend**
- Python 3.8+
- Flask (Web framework)
- SQLite (Database)
- scikit-learn (Machine learning)
- pandas & NumPy (Data processing)

**Frontend**
- HTML5/CSS3
- JavaScript (Vanilla)
- Responsive design

**DevOps**
- Git version control
- RESTful API design
- Comprehensive documentation

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Quick Start
```bash
# 1. Clone the repository
git clone https://github.com/kelechiodoemelam/clinical-early-warning-system.git
cd clinical-early-warning-system

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python app.py
```

The application will start on `http://localhost:5000`

### Generate Sample Data

In a **separate terminal**:
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run data generator
python generate_data.py
```

Then refresh your browser to see live data!

---

## Usage

### API Endpoints

#### Health Check
```bash
GET /health
```

#### Ingest Patient Data
```bash
POST /api/ingest
Content-Type: application/json

{
  "patient_id": "P001",
  "age": 67,
  "gender": "M",
  "ward": "ICU",
  "source_system": "ICU_Monitor_System",
  "heart_rate": 85,
  "bp_systolic": 120,
  "bp_diastolic": 80,
  "respiratory_rate": 16,
  "temperature": 37.2,
  "oxygen_saturation": 98
}
```

#### Get All Patients
```bash
GET /api/patients
```

#### Get Patient Vitals
```bash
GET /api/vitals/{patient_id}
```

#### Generate Risk Prediction
```bash
POST /api/predict/{patient_id}
```

#### Dashboard Data
```bash
GET /api/dashboard
```

---

## Machine Learning Model

### Algorithm: Random Forest Classifier

**Configuration:**
- **Estimators**: 100 decision trees
- **Max Depth**: 10 (prevents overfitting)
- **Class Weighting**: Balanced (handles imbalanced data)
- **Random State**: 42 (reproducibility)

### Features (6 vital signs)
1. Heart Rate (bpm)
2. Blood Pressure Systolic (mmHg)
3. Blood Pressure Diastolic (mmHg)
4. Respiratory Rate (breaths/min)
5. Temperature (°C)
6. Oxygen Saturation (%)

### Risk Prediction Thresholds
- **HIGH RISK**: Probability > 0.7 (immediate attention)
- **MEDIUM RISK**: Probability 0.4-0.7 (enhanced monitoring)
- **LOW RISK**: Probability < 0.4 (routine monitoring)

### Why Random Forest?
- Handles non-linear relationships in vital signs
- Resistant to overfitting with proper tuning
- Provides feature importance for clinical explainability
- Proven in medical literature for risk assessment

---

## 🔐 Data Protection & GDPR Compliance

### Anonymization
```python
anonymized_id = SHA-256(patient_id)[:16]
```
- One-way hash function (irreversible)
- Consistent mapping (same patient = same anonymous ID)
- No personally identifiable information stored

### Audit Logging
All actions recorded with:
- Timestamp
- Action type (DATA_INGEST, PREDICTION, DATA_ACCESS)
- User/System ID
- Anonymized patient ID
- Action details

### Security Measures
- Input validation on all API endpoints
- SQL injection prevention (parameterized queries)
- Error handling prevents information leakage
- CORS configured for controlled access

---

## 📚 Project Background

### Academic Foundation
This project builds upon my **MSc Information Technology (Distinction)** final project on **failure prediction for offshore wind turbines** using machine learning.

### Translation to Healthcare

| Wind Turbine Project | Clinical Application |
|---------------------|---------------------|
| Sensor data from turbines | Vital signs from patients |
| Predict equipment failure | Predict patient deterioration |
| Low-incident events (5% failures) | Low-incident events (5% deterioration) |
| Random Forest for imbalanced data | Random Forest for imbalanced data |
| Preventive maintenance | Early clinical intervention |

### Purpose
Built as a portfolio piece to demonstrate data engineering capabilities for NHS Secure Data Environment roles, specifically the Thames Valley & Surrey SDE Programme.

---

## 🎯 Future Enhancements

### Technical Improvements
- [ ] PostgreSQL migration for production scale
- [ ] Docker containerization
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Comprehensive test suite
- [ ] API authentication (OAuth2/JWT)
- [ ] Real-time streaming with Apache Kafka

### Feature Additions
- [ ] HL7/FHIR data format support
- [ ] Advanced visualizations (time-series charts)
- [ ] Alert notification system
- [ ] Multi-tenancy for different hospitals
- [ ] Mobile responsive dashboard

### ML Improvements
- [ ] XGBoost model comparison
- [ ] LSTM for time-series prediction
- [ ] Model explainability (SHAP values)
- [ ] Continuous learning pipeline

---

## 📝 Database Schema

### Tables

**patients**
- patient_id (PRIMARY KEY)
- age
- gender
- admission_date
- ward
- anonymized_id

**vital_signs**
- record_id (PRIMARY KEY)
- patient_id (FOREIGN KEY)
- timestamp
- heart_rate
- blood_pressure_systolic
- blood_pressure_diastolic
- respiratory_rate
- temperature
- oxygen_saturation
- source_system

**risk_predictions**
- prediction_id (PRIMARY KEY)
- patient_id (FOREIGN KEY)
- timestamp
- risk_score
- risk_level
- contributing_factors

**audit_log**
- log_id (PRIMARY KEY)
- timestamp
- action
- user_id
- patient_id
- details

---

## 👤 Author

**Kelechi Odoemelam**
- MSc Information Technology (Distinction)
- Specialization: Data Engineering & Machine Learning
- GitHub: [@kelechiodoemelam](https://github.com/kelechiodoemelam)


---


---

## 📞 Contact

For questions about this project or to discuss data engineering opportunities:
- GitHub: [@kelechiodoemelam](https://github.com/kelechiodoemelam)
- Project Repository: [clinical-early-warning-system](https://github.com/kelechiodoemelam/clinical-early-warning-system)
