import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
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

# Dividir o dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

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
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(random_state=0))
])

# Definir parâmetros para Grid Search
param_grid = {
    'regressor__n_estimators': [50, 100, 150, 200],
    'regressor__max_depth': [None, 10, 20, 30],
    'regressor__min_samples_split': [2, 5, 10],
    'regressor__min_samples_leaf': [1, 2, 4],
    'regressor__bootstrap': [True, False]
}

# Configurar Grid Search
grid_search = GridSearchCV(estimator=pipeline, param_grid=param_grid, 
                           cv=3, n_jobs=-1, verbose=2, scoring='neg_mean_squared_error')

# Executar Grid Search
grid_search.fit(X_train, y_train)

# Melhor modelo
best_model = grid_search.best_estimator_

# Imprimir os melhores parâmetros encontrados
print(f"Melhores parâmetros encontrados: {grid_search.best_params_}")

# Salvar os melhores parâmetros em um arquivo de texto
metrics_folder = get_next_metricas_folder()
os.makedirs(metrics_folder, exist_ok=True)
with open(f'{metrics_folder}/best_params.txt', 'w') as file:
    file.write(f"Melhores parâmetros encontrados:\n")
    for param, value in grid_search.best_params_.items():
        file.write(f"{param}: {value}\n")

# Fazer previsões com o pipeline ajustado
y_pred = best_model.predict(X_test)

# Calcular MSE e RMSE
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print(f'Mean Squared Error: {mse}')
print(f'Root Mean Squared Error: {rmse}')

# Criar pastas se não existirem
os.makedirs('trainedModel', exist_ok=True)

# Salvar o modelo em um arquivo
joblib.dump(best_model, 'trainedModel/flight_duration_model.pkl')
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
plt.figure(figsize=(8, 6))

# Plotar distribuição das durações reais
plt.hist(df['Duration'], bins=30, edgecolor='k', alpha=0.7)
plt.title('Distribuição da Duração Original')
plt.xlabel('Duração')
plt.ylabel('Frequência')

# Salvar o gráfico
plt.tight_layout()
plt.savefig(f'{metrics_folder}/data_distribution.png')
# plt.show()
