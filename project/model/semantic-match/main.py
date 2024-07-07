from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
from fastapi.middleware.cors import CORSMiddleware
import os
import pickle

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    text: str
    top_x: int

# Read the metadata CSV file
df_metadata = pd.read_csv('videoid_and_metadata.csv')

# Read the transcriptions CSV file
df_transcriptions = pd.read_csv('transcriptions.csv')

# Merge the two DataFrames on the 'id' column
df = pd.merge(df_metadata, df_transcriptions, on='id')

# Concatenate the 'metadata' and 'Text' fields
df['combined_text'] = df['metadata'] + ' ' + df['Text']
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
model = AutoModel.from_pretrained('distilbert-base-uncased')

def preprocess_text(text):
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    import nltk

    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalnum()]
    tokens = [word.lower() for word in tokens if word.lower() not in stop_words]
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(lemmatized_tokens)

def embed_text(text):
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
embeddings_file = os.path.join(os.path.dirname(__file__), 'pickle-files/embeddings.pkl')
if os.path.exists(embeddings_file):
    with open(embeddings_file, 'rb') as f:
        embeddings_dict = pickle.load(f)
    df_embeddings = pd.DataFrame(embeddings_dict)
    df_embeddings['embedding'] = df_embeddings['embedding'].apply(np.array)
else:
    df['embedding'] = df['combined_text'].apply(embed_text)
    with open(embeddings_file, 'wb') as f:
        pickle.dump(df[['id', 'embedding']].to_dict(), f)
    df_embeddings = df[['id', 'embedding']]

df = pd.merge(df, df_embeddings, on='id', how='left')

@app.post("/query")
def query(request: QueryRequest):
    try:
        generated_text = request.text
        top_x = request.top_x
        top_matches = find_top_matches(generated_text, df, top_x)
        return top_matches.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

# To run the server with Mangum for AWS Lambda
from mangum import Mangum
handler = Mangum(app)