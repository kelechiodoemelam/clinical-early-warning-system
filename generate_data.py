"""
Clinical Data Generator
Simulates data from multiple hospital systems (ICU, A&E, Wards)
Demonstrates data integration from diverse sources
"""

import requests
import random
import time
from datetime import datetime

# Simulate different hospital systems
SYSTEMS = ['ICU_Monitor_System', 'A&E_Triage_System', 'Ward_Vitals_System']

# Sample patient data
PATIENTS = [
    {'patient_id': 'P001', 'age': 67, 'gender': 'M', 'ward': 'ICU'},
    {'patient_id': 'P002', 'age': 45, 'gender': 'F', 'ward': 'A&E'},
    {'patient_id': 'P003', 'age': 82, 'gender': 'F', 'ward': 'Ward 3'},
    {'patient_id': 'P004', 'age': 54, 'gender': 'M', 'ward': 'ICU'},
    {'patient_id': 'P005', 'age': 39, 'gender': 'F', 'ward': 'Ward 2'},
    {'patient_id': 'P006', 'age': 71, 'gender': 'M', 'ward': 'A&E'},
    {'patient_id': 'P007', 'age': 28, 'gender': 'F', 'ward': 'Ward 1'},
    {'patient_id': 'P008', 'age': 63, 'gender': 'M', 'ward': 'ICU'},
]

def generate_vitals(base_stable=True):
    """
    Generate realistic vital signs
    base_stable=False creates more abnormal readings (for testing risk detection)
    """
    if base_stable:
        # Normal ranges
        heart_rate = random.randint(60, 100)
        bp_systolic = random.randint(110, 140)
        bp_diastolic = random.randint(70, 90)
        respiratory_rate = random.randint(12, 20)
        temperature = round(random.uniform(36.5, 37.5), 1)
        oxygen_saturation = random.randint(95, 100)
    else:
        # Abnormal ranges (high risk)
        heart_rate = random.randint(40, 55) if random.random() > 0.5 else random.randint(120, 160)
        bp_systolic = random.randint(80, 100) if random.random() > 0.5 else random.randint(160, 200)
        bp_diastolic = random.randint(50, 65) if random.random() > 0.5 else random.randint(95, 120)
        respiratory_rate = random.randint(8, 10) if random.random() > 0.5 else random.randint(25, 35)
        temperature = round(random.uniform(35.0, 36.0), 1) if random.random() > 0.5 else round(random.uniform(38.5, 40.0), 1)
        oxygen_saturation = random.randint(85, 93)
    
    return {
        'heart_rate': heart_rate,
        'bp_systolic': bp_systolic,
        'bp_diastolic': bp_diastolic,
        'respiratory_rate': respiratory_rate,
        'temperature': temperature,
        'oxygen_saturation': oxygen_saturation
    }

def send_data(patient, vitals, source_system):
    """Send data to the ingestion API"""
    data = {
        'patient_id': patient['patient_id'],
        'age': patient['age'],
        'gender': patient['gender'],
        'ward': patient['ward'],
        'source_system': source_system,
        **vitals
    }
    
    try:
        response = requests.post('http://localhost:5000/api/ingest', json=data)
        if response.status_code == 201:
            print(f"✓ Data sent for {patient['patient_id']} from {source_system}")
            return True
        else:
            print(f"✗ Error for {patient['patient_id']}: {response.json()}")
            return False
    except Exception as e:
        print(f"✗ Connection error: {str(e)}")
        return False

def generate_predictions():
    """Generate risk predictions for all patients"""
    print("\n--- Generating Risk Predictions ---")
    for patient in PATIENTS:
        try:
            response = requests.post(f'http://localhost:5000/api/predict/{patient["patient_id"]}')
            if response.status_code == 200:
                result = response.json()
                risk_emoji = "🔴" if result['risk_level'] == 'HIGH' else "🟡" if result['risk_level'] == 'MEDIUM' else "🟢"
                print(f"{risk_emoji} {patient['patient_id']}: {result['risk_level']} (Score: {result['risk_score']:.2f})")
            else:
                print(f"✗ Prediction failed for {patient['patient_id']}")
        except Exception as e:
            print(f"✗ Error predicting for {patient['patient_id']}: {str(e)}")

def simulate_data_streams(rounds=3):
    """
    Simulate continuous data ingestion from multiple hospital systems
    """
    print("=== Clinical Data Integration Simulation ===")
    print(f"Simulating {len(SYSTEMS)} different hospital systems")
    print(f"Monitoring {len(PATIENTS)} patients\n")
    
    for round_num in range(1, rounds + 1):
        print(f"\n--- Round {round_num}: Data Collection Cycle ---")
        
        for patient in PATIENTS:
            # Randomly select a source system
            source = random.choice(SYSTEMS)
            
            # 20% chance of abnormal vitals for some patients (to test risk detection)
            is_stable = random.random() > 0.2 if patient['ward'] == 'ICU' else random.random() > 0.1
            vitals = generate_vitals(base_stable=is_stable)
            
            send_data(patient, vitals, source)
            time.sleep(0.2)  # Small delay to simulate real-time ingestion
        
        # Generate predictions after each round
        time.sleep(1)
        generate_predictions()
        
        if round_num < rounds:
            print(f"\nWaiting 3 seconds before next round...\n")
            time.sleep(3)
    
    print("\n=== Simulation Complete ===")
    print(f"Total data points generated: {len(PATIENTS) * rounds}")
    print(f"Data integrated from {len(SYSTEMS)} different systems")
    print("\nYou can now view the dashboard at: http://localhost:5000")

if __name__ == '__main__':
    print("Starting Clinical Data Generator...")
    print("Make sure the Flask app is running on http://localhost:5000\n")
    
    time.sleep(2)
    
    # Run simulation
    simulate_data_streams(rounds=5)



