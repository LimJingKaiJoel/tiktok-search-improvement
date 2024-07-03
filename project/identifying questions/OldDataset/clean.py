import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(current_dir, 'TrainingData.csv')
output_file = os.path.join(current_dir, 'TrainingDataQuestions.csv')

try:
    df = pd.read_csv(input_file)
except Exception as e:
    print(f"Error reading {input_file}: {e}")
    exit(1)

if 'question' not in df.columns:
    print("Error: 'question' column not found in the CSV file.")
    exit(1)


questions_df = df[['question']]
questions_df = questions_df[questions_df['question'].notna()]

questions_df.to_csv(output_file, index=False)
print(f"Questions have been saved to {output_file}")
