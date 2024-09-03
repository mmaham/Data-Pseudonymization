import pandas as pd
import hashlib


def pseudonymize_data(data):
    # Pseudonymize sensitive columns using hashing
    pseudonymized_data = data.copy()
    sensitive_columns = ['Name', 'Doctor', 'Hospital', 'Room Number']  # Example sensitive columns

    for column in sensitive_columns:
        pseudonymized_data[column] = pseudonymized_data[column].apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest())

    return pseudonymized_data


# Load dataset
dataset_path = 'Healthcare_Data.csv'
data = pd.read_csv(dataset_path)

# Pseudonymize data
pseudonymized_data = pseudonymize_data(data)

# Save pseudonymized data to a new CSV file
output_path = 'pseudonymized_data.csv'
pseudonymized_data.to_csv(output_path, index=False)

print("Data pseudonymization completed. Pseudonymized dataset saved to:", output_path)
