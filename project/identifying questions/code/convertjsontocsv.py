import json
import csv
import os

# todo: strip whitespace from nonquestions column
json_file_path = '/Users/joellim/iCloud Drive (Archive)/Desktop/tiktok techjam/identifying questions/dev-v2.0.json'
tsv_file_path = '/Users/joellim/iCloud Drive (Archive)/Desktop/tiktok techjam/identifying questions/nonquestions.tsv'
csv_file_path = '/Users/joellim/iCloud Drive (Archive)/Desktop/tiktok techjam/identifying questions/TrainingData.csv'


def json_to_list(json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
    
        rows = []

        for item in data['data']:
            for paragraph in item['paragraphs']:
                for qa in paragraph['qas']:
                    question = qa['question']
                    if question.endswith('?'):
                        question = question[:-1]
                    
                    rows.append(question)
        return rows     
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
def extract_non_questions(tsv_file_path):
    non_questions = []
    try:
        with open(tsv_file_path, 'r') as tsv_file:
            reader = csv.reader(tsv_file, delimiter='\t')
            for row in reader:
                if row:
                    sentence = row[0]
                    non_questions.append(sentence)
        
        print(f"Extracted {len(non_questions)} non-questions from TSV file.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return non_questions

def merge_into_csv(questions, non_questions, csv_file_path):
    try:
        with open(csv_file_path, 'w', newline='') as csv_file:
            fieldnames = ["question", "non question"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            
            max_length = max(len(questions), len(non_questions))
            
            questions.extend([''] * (max_length - len(questions)))
            non_questions.extend([''] * (max_length - len(non_questions)))
            
            for question, non_question in zip(questions, non_questions):
                writer.writerow({"question": question, "non question": non_question})
        
        print(f"Questions and non-questions merged into CSV file saved as {csv_file_path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

questions = json_to_list(json_file_path)
non_questions = extract_non_questions(tsv_file_path)

merge_into_csv(questions, non_questions, csv_file_path)