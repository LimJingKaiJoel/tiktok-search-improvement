import pandas as pd
import os

# Specify the directory and file names
current_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(current_dir, 'TrainingData.csv')
output_file = os.path.join(current_dir, 'TrainingDataQuestions.csv')

# Load the CSV file
try:
    df = pd.read_csv(input_file)  # Adjust encoding if needed
except Exception as e:
    print(f"Error reading {input_file}: {e}")
    exit(1)

# Filter out the rows where the 'question' column is not empty
questions_df = df[df['question'].notna()]
df.head()
# Save the filtered rows to a new CSV file
questions_df.to_csv(output_file, index=False)

print(f"Questions have been saved to {output_file}")
