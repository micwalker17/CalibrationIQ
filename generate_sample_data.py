import pandas as pd

def generate_data():
    """Generates a sample CSV file with realistic measurement data."""
    data = {
        'job_number': ['WO-001', 'WO-001', 'WO-002', 'WO-002', 'WO-003', 'WO-004', 'WO-004'],
        'sample_serial_number': ['SN-101', 'SN-101', 'SN-201', 'SN-201', 'SN-301', 'SN-401', 'SN-401'],
        'dimension_id': ['Char 1', 'Char 2', 'Char 5', 'Char 6', 'Char 9', 'Char 12', 'Char 15'],
        'feature_name': ['Hole Diameter', 'Step Height', 'Outer Diameter', 'Groove Depth', 'Slot Width', 'Pin Diameter', 'Boss Height'],
        'measured_value': [0.5005, 1.2510, 3.0001, 0.1008, 0.7511, 0.2498, 1.5003],
        'nominal_value': [0.5000, 1.2500, 3.0000, 0.1000, 0.7500, 0.2500, 1.5000],
        'original_upper_tol': [0.5010, 1.2520, 3.0005, 0.1010, 0.7510, 0.2505, 1.5005],
        'original_lower_tol': [0.4990, 1.2480, 2.9995, 0.0990, 0.7490, 0.2495, 1.4995],
        'tolerance_type': ['BILATERAL', 'BILATERAL', 'BILATERAL', 'BILATERAL', 'BILATERAL', 'BILATERAL', 'BILATERAL'],
        'criticality': ['Critical', 'Major', 'NotSpecified', 'NotSpecified', 'Minor', 'Critical', 'Minor']
    }
    df = pd.DataFrame(data)
    
    output_path = 'sample_measurements.csv'
    df.to_csv(output_path, index=False)
    
    print(f"✅ Sample data generated and saved to '{output_path}'")

if __name__ == "__main__":
    generate_data()
