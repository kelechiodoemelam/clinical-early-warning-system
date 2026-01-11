"""
Clinical Early Warning System - Main Application
A healthcare data integration platform with predictive analytics

Author: [Kelechi Odoemelam]
Purpose: Portfolio project demonstrating data engineering for NHS SDE role
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import sqlite3
import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os

app = Flask(__name__)
CORS(app)

# Database initialization
def init_db():
    """Initialize SQLite database with clinical data schema"""
    conn = sqlite3.connect('clinical_data.db')
    c = conn.cursor()
    
    # Patient demographics table
    c.execute('''CREATE TABLE IF NOT EXISTS patients
                 (patient_id TEXT PRIMARY KEY,
                  age INTEGER,
                  gender TEXT,
                  admission_date TEXT,
                  ward TEXT,
                  anonymized_id TEXT)''')
    
    # Vital signs table (time-series data)
    c.execute('''CREATE TABLE IF NOT EXISTS vital_signs
                 (record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  patient_id TEXT,
                  timestamp TEXT,
                  heart_rate INTEGER,
                  blood_pressure_systolic INTEGER,
                  blood_pressure_diastolic INTEGER,
                  respiratory_rate INTEGER,
                  temperature REAL,
                  oxygen_saturation INTEGER,
                  source_system TEXT,
                  FOREIGN KEY(patient_id) REFERENCES patients(patient_id))''')
    
    # Risk predictions table
    c.execute('''CREATE TABLE IF NOT EXISTS risk_predictions
                 (prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  patient_id TEXT,
                  timestamp TEXT,
                  risk_score REAL,
                  risk_level TEXT,
                  contributing_factors TEXT,
                  FOREIGN KEY(patient_id) REFERENCES patients(patient_id))''')
    
    # Audit log for data governance
    c.execute('''CREATE TABLE IF NOT EXISTS audit_log
                 (log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT,
                  action TEXT,
                  user_id TEXT,
                  patient_id TEXT,
                  details TEXT)''')
    
    conn.commit()
    conn.close()

# Anonymization function (GDPR compliance)
def anonymize_patient_id(patient_id):
    """Generate anonymized ID for patient (demonstrates data protection awareness)"""
    import hashlib
    return hashlib.sha256(patient_id.encode()).hexdigest()[:16]

# Data ingestion endpoint
@app.route('/api/ingest', methods=['POST'])
def ingest_data():
    """
    Ingest data from various clinical systems
    Accepts JSON data with patient vitals
    """
    try:
        data = request.json
        source_system = data.get('source_system', 'unknown')
        
        conn = sqlite3.connect('clinical_data.db')
        c = conn.cursor()
        
        # Validate and insert patient if new
        patient_id = data['patient_id']
        anonymized_id = anonymize_patient_id(patient_id)
        
        c.execute('SELECT patient_id FROM patients WHERE patient_id = ?', (patient_id,))
        if not c.fetchone():
            c.execute('''INSERT INTO patients 
                        (patient_id, age, gender, admission_date, ward, anonymized_id)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                     (patient_id, data.get('age'), data.get('gender'), 
                      datetime.now().isoformat(), data.get('ward'), anonymized_id))
        
        # Insert vital signs
        c.execute('''INSERT INTO vital_signs 
                    (patient_id, timestamp, heart_rate, blood_pressure_systolic,
                     blood_pressure_diastolic, respiratory_rate, temperature,
                     oxygen_saturation, source_system)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (patient_id, datetime.now().isoformat(), 
                  data.get('heart_rate'), data.get('bp_systolic'),
                  data.get('bp_diastolic'), data.get('respiratory_rate'),
                  data.get('temperature'), data.get('oxygen_saturation'),
                  source_system))
        
        # Audit logging
        c.execute('''INSERT INTO audit_log 
                    (timestamp, action, user_id, patient_id, details)
                    VALUES (?, ?, ?, ?, ?)''',
                 (datetime.now().isoformat(), 'DATA_INGEST', 'system', 
                  anonymized_id, f'Source: {source_system}'))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Data ingested successfully',
            'anonymized_id': anonymized_id
        }), 201
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

# Get patient data (anonymized)
@app.route('/api/patients', methods=['GET'])
def get_patients():
    """Retrieve all patients with anonymized IDs"""
    try:
        conn = sqlite3.connect('clinical_data.db')
        
        query = '''SELECT anonymized_id, age, gender, ward, admission_date
                   FROM patients
                   ORDER BY admission_date DESC'''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return jsonify(df.to_dict('records')), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Get vital signs for a patient
@app.route('/api/vitals/<patient_id>', methods=['GET'])
def get_vitals(patient_id):
    """Retrieve vital signs history for a specific patient"""
    try:
        conn = sqlite3.connect('clinical_data.db')
        
        query = '''SELECT timestamp, heart_rate, blood_pressure_systolic,
                          blood_pressure_diastolic, respiratory_rate, 
                          temperature, oxygen_saturation, source_system
                   FROM vital_signs
                   WHERE patient_id = ?
                   ORDER BY timestamp DESC
                   LIMIT 50'''
        
        df = pd.read_sql_query(query, conn, params=(patient_id,))
        conn.close()
        
        return jsonify(df.to_dict('records')), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Predictive model functions (adapted from your wind turbine work)
def train_risk_model():
    """
    Train a Random Forest model for patient risk prediction
    This simulates your wind turbine failure prediction approach
    """
    # Generate synthetic training data (in real scenario, this would be historical data)
    np.random.seed(42)
    n_samples = 1000
    
    # Features: normalized vital signs
    X = np.random.randn(n_samples, 6)  # 6 vital sign features
    
    # Target: risk of deterioration (1 = high risk, 0 = stable)
    # Simulate imbalanced dataset (like your low-incident wind turbine data)
    y = np.zeros(n_samples)
    high_risk_indices = np.random.choice(n_samples, size=int(n_samples * 0.05), replace=False)
    y[high_risk_indices] = 1
    
    # Train Random Forest (your proven approach)
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        class_weight='balanced',  # Handle imbalanced data
        random_state=42
    )
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model.fit(X_scaled, y)
    
    # Save model and scaler
    with open('risk_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    return model, scaler

def predict_patient_risk(patient_id):
    """
    Predict risk level for a patient based on latest vitals
    Uses Random Forest model (your demonstrated expertise)
    """
    try:
        # Load model (train if not exists)
        if not os.path.exists('risk_model.pkl'):
            train_risk_model()
        
        with open('risk_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        
        # Get latest vitals
        conn = sqlite3.connect('clinical_data.db')
        query = '''SELECT heart_rate, blood_pressure_systolic, 
                          blood_pressure_diastolic, respiratory_rate,
                          temperature, oxygen_saturation
                   FROM vital_signs
                   WHERE patient_id = ?
                   ORDER BY timestamp DESC
                   LIMIT 1'''
        
        df = pd.read_sql_query(query, conn, params=(patient_id,))
        
        if df.empty:
            return None
        
        # Prepare features
        features = df.values[0]
        features_scaled = scaler.transform([features])
        
        # Predict
        risk_proba = model.predict_proba(features_scaled)[0][1]
        
        # Determine risk level
        if risk_proba > 0.7:
            risk_level = 'HIGH'
        elif risk_proba > 0.4:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        # Feature importance for explanation
        feature_names = ['heart_rate', 'bp_systolic', 'bp_diastolic', 
                        'respiratory_rate', 'temperature', 'oxygen_saturation']
        importances = model.feature_importances_
        contributing_factors = [f"{name}: {imp:.2f}" 
                              for name, imp in zip(feature_names, importances)]
        
        # Save prediction
        c = conn.cursor()
        c.execute('''INSERT INTO risk_predictions
                    (patient_id, timestamp, risk_score, risk_level, contributing_factors)
                    VALUES (?, ?, ?, ?, ?)''',
                 (patient_id, datetime.now().isoformat(), 
                  float(risk_proba), risk_level, json.dumps(contributing_factors)))
        conn.commit()
        conn.close()
        
        return {
            'risk_score': float(risk_proba),
            'risk_level': risk_level,
            'contributing_factors': contributing_factors
        }
        
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return None

# Risk prediction endpoint
@app.route('/api/predict/<patient_id>', methods=['POST'])
def predict_risk(patient_id):
    """Generate risk prediction for a patient"""
    result = predict_patient_risk(patient_id)
    
    if result:
        return jsonify(result), 200
    else:
        return jsonify({'status': 'error', 'message': 'Unable to generate prediction'}), 400

# Dashboard endpoint
@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    """Get overview data for dashboard"""
    try:
        conn = sqlite3.connect('clinical_data.db')
        
        # Get stats
        stats = {}
        
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM patients')
        stats['total_patients'] = c.fetchone()[0]
        
        c.execute('SELECT COUNT(*) FROM vital_signs WHERE date(timestamp) = date("now")')
        stats['readings_today'] = c.fetchone()[0]
        
        c.execute('''SELECT COUNT(*) FROM risk_predictions 
                    WHERE risk_level = "HIGH" AND date(timestamp) = date("now")''')
        stats['high_risk_patients'] = c.fetchone()[0]
        
        # Get recent predictions
        query = '''SELECT p.anonymized_id, rp.risk_level, rp.risk_score, rp.timestamp
                   FROM risk_predictions rp
                   JOIN patients p ON rp.patient_id = p.patient_id
                   ORDER BY rp.timestamp DESC
                   LIMIT 10'''
        
        df = pd.read_sql_query(query, conn)
        stats['recent_predictions'] = df.to_dict('records')
        
        conn.close()
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

# Home route
@app.route('/')
def home():
    """Serve the dashboard"""
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    print("Clinical Early Warning System starting...")
    print("Initializing database and training risk model...")
    train_risk_model()
    print("System ready!")
    app.run(debug=True, port=5000)