import pandas as pd
import joblib

# Load the trained model from file
model = joblib.load('flight_duration_model.pkl')
print("Model loaded from 'flight_duration_model.pkl'")

# Example data for prediction
example_data = pd.DataFrame({
    'OriginCode': ['JFK'],
    'DestinCode': ['LAX'],
    'WeekDay': [3], 
    'HourDeparture': [14],  # e.g., 2 PM
    'ModelAircraft': ['B737']
})

# Predict flight duration
predicted_duration = model.predict(example_data)
print(f'Predicted Duration: {predicted_duration[0]:.2f} minutes')
