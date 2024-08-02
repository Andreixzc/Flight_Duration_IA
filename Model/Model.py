import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib  # Import joblib for saving the model

# Load the dataset
df = pd.read_csv('../Dataset/trainingFlightTable.csv')

# Display the first few rows of the dataframe
print(df.head())

# Define features and target
X = df[['OriginCode', 'DestinCode', 'WeekDay', 'HourDeparture', 'ModelAircraft']]
y = df['Duration']

# Preprocessing for numeric features
numeric_features = ['WeekDay', 'HourDeparture']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])

# Preprocessing for categorical features
categorical_features = ['OriginCode', 'DestinCode', 'ModelAircraft']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

# Combine preprocessing for both numeric and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])

# Define the model pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=0))])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Save the model to a file
joblib.dump(model, 'flight_duration_model.pkl')
print("Model saved to 'flight_duration_model.pkl'")

# Save predictions and actual values to a text file
with open('predictions_vs_actual.csv', 'w') as file:
    file.write('Actual Duration, Predicted Duration\n')
    for actual, predicted in zip(y_test, y_pred):
        file.write(f'{actual:.2f}, {predicted:.2f}\n')

# Example data for prediction (Uncomment to use)
# example_data = pd.DataFrame({
#     'OriginCode': ['JFK'],
#     'DestinCode': ['LAX'],
#     'WeekDay': [3],
#     'HourDeparture': [14],
#     'ModelAircraft': ['B737']
# })

# # Predict flight duration
# predicted_duration = model.predict(example_data)
# print(f'Predicted Duration: {predicted_duration[0]} minutes')
