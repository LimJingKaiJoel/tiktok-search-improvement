import pandas as pd
import os
import sys

# Specify the directory containing the CSV files
current_dir = os.path.dirname(os.path.abspath(__file__))

dataset_dir = os.path.join(current_dir, 'KaggleDataset')
output_file = os.path.join(current_dir, 'TrainingDataNonQuestions.csv')

if os.path.exists(output_file):
    print(f"Error: The file '{output_file}' already exists.")
    sys.exit(1)


# List to hold data from all CSV files
all_data = []

# Loop through each file in the directory
for filename in os.listdir(dataset_dir):
    if filename.endswith('.csv'):
        # Full path to the CSV file
        file_path = os.path.join(dataset_dir, filename)
        
        # Load the CSV file
        try:
            df = pd.read_csv(file_path, encoding='latin1')  # Adjust encoding if needed
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue
        
        # Select columns '1' to '20'
        columns_of_interest = [str(i) for i in range(1, 21)]
        selected_data = df[columns_of_interest]
        
        # Convert all values to lowercase
        selected_data = selected_data.applymap(lambda x: str(x).lower() if pd.notnull(x) else x)
        
        # Append the selected data to the list
        all_data.append(selected_data)

# Concatenate all data into a single DataFrame
combined_data = pd.concat(all_data, ignore_index=True)

# Extract unique values from the selected columns
unique_values = set()
for col in combined_data.columns:
    unique_values.update(combined_data[col].unique())

# Remove NaN values from the set of unique values
unique_values.discard('nan')

# Convert the set to a DataFrame
unique_values_df = pd.DataFrame(list(unique_values), columns=['non question'])

# Save the unique values to a new CSV file
unique_values_df.to_csv(output_file, index=False)

print(f"Unique values have been saved to {output_file}")
