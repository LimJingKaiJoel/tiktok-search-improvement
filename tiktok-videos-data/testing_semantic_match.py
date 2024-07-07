import pandas as pd
import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import time
import pickle
import os

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

start_time = time.time()

# Read the metadata CSV file
df_metadata = pd.read_csv('tiktok-videos-data/videoid_and_metadata.csv')

# Read the transcriptions CSV file
df_transcriptions = pd.read_csv('tiktok-videos-data/transcriptions.csv')

# Merge the two DataFrames on the 'id' column
df = pd.merge(df_metadata, df_transcriptions, on='id')

# Concatenate the 'metadata' and 'Text' fields
df['combined_text'] = df['metadata'] + ' ' + df['Text']

tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
model = AutoModel.from_pretrained('distilbert-base-uncased')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalnum()]
    tokens = [word.lower() for word in tokens if word.lower() not in stop_words]
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(lemmatized_tokens)

def embed_text(text):
    # NOTE: change comment to unpreprocess the text
    processed_text = preprocess_text(text)
    inputs = tokenizer(processed_text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

def find_top_matches(generated_text, df, top_x):
    generated_embedding = embed_text(generated_text)
    similarities = cosine_similarity(
        [generated_embedding],
        np.stack(df['embedding'].values)
    )[0]
    top_indices = similarities.argsort()[-top_x:][::-1]

    # Select the relevant columns for the top matches
    top_matches = df.iloc[top_indices][['id', 'good result', 'combined_text']].copy()
    top_matches['similarity'] = similarities[top_indices]
    return top_matches

# Check if embeddings file exists
# NOTE: if you change something, you might have to delete pkl file and rerun code to generate new pkl
embeddings_file = 'embeddings.pkl'
if os.path.exists(embeddings_file):
    with open(embeddings_file, 'rb') as f:
        embeddings_dict = pickle.load(f)
    df_embeddings = pd.DataFrame(embeddings_dict)
    df_embeddings['embedding'] = df_embeddings['embedding'].apply(np.array)
else:
    # Embed and save embeddings if not already saved
    # NOTE: PREPROCESSED in embed_text method (seems like better accuracy)
    df['embedding'] = df['combined_text'].apply(embed_text)
    with open(embeddings_file, 'wb') as f:
        pickle.dump(df[['id', 'embedding']].to_dict(), f)
    df_embeddings = df[['id', 'embedding']]

df = pd.merge(df, df_embeddings, on='id', how='left')

# NOTE: Vince pls move the query answer by the LLM to replace this generated text if query is a question
generated_text = "To win a hackathon, focus on addressing the problem statement creatively and effectively, ensuring your solution is feasible and well-executed, and clearly communicate your project's value and impact to the judges. Prioritize teamwork, efficient time management, and leveraging each team member's strengths."

top_x = 5

# NOTE: call this find_top_matches function to get the id of the videos that we want to recommend
top_matches = find_top_matches(generated_text, df, top_x)
print(top_matches)

end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken: {time_taken} seconds")
