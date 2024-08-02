import pandas as pd
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the predictions and actual values from the CSV file
file_path = 'predictions_vs_actual.csv'

# Read the file into a DataFrame
df = pd.read_csv(file_path)

# Remove any leading/trailing whitespace from column names
df.columns = df.columns.str.strip()
print("Columns in the DataFrame:", df.columns)

# Extract the actual and predicted values
try:
    actual_values = df['Actual Duration']
    predicted_values = df['Predicted Duration']
except KeyError as e:
    print(f"Column not found: {e}")
    raise

# Calculate Mean Squared Error
mse = mean_squared_error(actual_values, predicted_values)
print(f'Mean Squared Error: {mse} minutes²')

# Calculate Root Mean Squared Error
rmse = np.sqrt(mse)
print(f'Root Mean Squared Error: {rmse} minutes')
