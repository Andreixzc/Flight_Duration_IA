import pandas as pd
import joblib

# Carregar o modelo treinado
model = joblib.load('trainedModel/flight_duration_model.pkl')
print("Model loaded from 'trainedModel/flight_duration_model.pkl'")

# Definir dados de exemplo
example_data = pd.DataFrame({
    'OriginCode': ['JFK'],
    'DestinCode': ['LAX'],
    'WeekDay': [3],
    'HourDeparture': [14],
    'ModelAircraft': ['B737']
})

# Fazer previsões com o modelo carregado
predicted_duration = model.predict(example_data)
print(f'Duracao Prevista: {predicted_duration[0]:.2f} minutos')
