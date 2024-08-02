import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib
import os
import numpy as np
import matplotlib.pyplot as plt

# Função para encontrar o próximo número de pasta disponível
def get_next_metricas_folder():
    base_path = 'metricas'
    i = 1
    while os.path.exists(f'{base_path}{i}'):
        i += 1
    return f'{base_path}{i}'

# Carregar o dataset
df = pd.read_csv('../Dataset/trainingFlightTable.csv')


# Definir características e alvo
X = df[['OriginCode', 'DestinCode', 'WeekDay', 'HourDeparture', 'ModelAircraft']]
y = df['Duration']

# Pipeline para tratar as variáveis numéricas
numeric_features = ['WeekDay', 'HourDeparture']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

# Pipeline para tratar as variáveis categóricas
categorical_features = ['OriginCode', 'DestinCode', 'ModelAircraft']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

# Combinar pré-processamento para dados numéricos e categóricos
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])

# Pipeline do modelo
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=0))])

# Dividir o dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Treinar o modelo
model.fit(X_train, y_train)

# Fazer previsões
y_pred = model.predict(X_test)

# Calcular MSE e RMSE
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print(f'Mean Squared Error: {mse}')
print(f'Root Mean Squared Error: {rmse}')

# Criar pastas se não existirem
os.makedirs('trainedModel', exist_ok=True)

# Obter o próximo número disponível para a pasta de métricas
metrics_folder = get_next_metricas_folder()
os.makedirs(metrics_folder, exist_ok=True)

# Salvar o modelo em um arquivo
joblib.dump(model, 'trainedModel/flight_duration_model.pkl')
print(f"Model saved to 'trainedModel/flight_duration_model.pkl'")

# Salvar MSE e RMSE em um arquivo de texto
with open(f'{metrics_folder}/metrics.txt', 'w') as file:
    file.write(f'Mean Squared Error: {mse}\n')
    file.write(f'Root Mean Squared Error: {rmse}\n')

# Salvar previsões e valores reais em um arquivo CSV
predictions_df = pd.DataFrame({
    'Actual Duration': y_test,
    'Predicted Duration': y_pred
})
predictions_df.to_csv(f'{metrics_folder}/predictions_vs_actual.csv', index=False)
print(f"Predictions and actual values saved to '{metrics_folder}/predictions_vs_actual.csv'")

# Plotar a distribuição dos dados
plt.figure(figsize=(12, 6))

# Plotar distribuição das durações reais
plt.subplot(1, 2, 1)
plt.hist(df['Duration'], bins=30, edgecolor='k', alpha=0.7)
plt.title('Distribuição da Duração Real')
plt.xlabel('Duração')
plt.ylabel('Frequência')

# Plotar distribuição das previsões
plt.subplot(1, 2, 2)
plt.hist(y_pred, bins=30, edgecolor='k', alpha=0.7)
plt.title('Distribuição da Duração Prevista')
plt.xlabel('Duração Prevista')
plt.ylabel('Frequência')

# Salvar o gráfico
plt.tight_layout()
plt.savefig(f'{metrics_folder}/data_distribution.png')
# plt.show()
