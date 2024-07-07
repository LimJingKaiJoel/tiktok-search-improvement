from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import torch
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
from fastapi.middleware.cors import CORSMiddleware
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import os
import pickle

# Download necessary NLTK resources

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

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
model = AutoModel.from_pretrained('distilbert-base-uncased')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Preprocess text function
def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalnum()]
    tokens = [word.lower() for word in tokens if word.lower() not in stop_words]
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(lemmatized_tokens)

# Embed text function
def embed_text(text):
    processed_text = preprocess_text(text)
    inputs = tokenizer(processed_text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

# Find top matches function
def find_top_matches(generated_text, df, top_x):
    generated_embedding = embed_text(generated_text)
    similarities = cosine_similarity(
        [generated_embedding],
        np.stack(df['embedding'].values)
    )[0]
    top_indices = similarities.argsort()[-top_x:][::-1]

    top_matches = df.iloc[top_indices][['id', 'good result', 'combined_text']].copy()
    top_matches['similarity'] = similarities[top_indices]
    return top_matches

# Load embeddings from pickle file
embeddings_file = 'pickle-files/embeddings.pkl'
if os.path.exists(embeddings_file):
    with open(embeddings_file, 'rb') as f:
        embeddings_dict = pickle.load(f)
    df_embeddings = pd.DataFrame(embeddings_dict)
    df_embeddings['embedding'] = df_embeddings['embedding'].apply(np.array)
else:
    raise FileNotFoundError("Embeddings file not found. Please ensure the embeddings.pkl file is present in the pickle-files directory.")

@app.post("/query")
def query(request: QueryRequest):
    try:
        generated_text = request.text
        top_x = 5
        top_matches = find_top_matches(generated_text, df_embeddings, top_x)
        return top_matches.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")

# To run the server with Mangum for AWS Lambda
from mangum import Mangum
handler = Mangum(app)
