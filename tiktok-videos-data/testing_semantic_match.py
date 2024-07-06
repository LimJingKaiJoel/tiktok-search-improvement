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

nltk.download('punkt')
start_time = time.time()

df = pd.read_csv('tiktok-videos-data/videoid_and_metadata.csv')

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

    # here oso change as needed for header
    top_matches = df.iloc[top_indices][['id', 'metadata', 'good result']].copy()
    top_matches['similarity'] = similarities[top_indices]
    return top_matches


# change df header as necessary 
df['processed'] = df['metadata'].apply(preprocess_text)
df['embedding'] = df['processed'].apply(embed_text)

# query or llm answer goes in here
generated_text = "hackathon, teamwork, presentation"



# # if including the query also (worse accuracy)
# query = "how do i win a hackathon?"
# generated_text = query + " " + generated_text

top_x = 5

top_matches = find_top_matches(generated_text, df, top_x)
print(top_matches)

# for vince: TO EXTRACT THE ID: CALL top_matches['id'] (but it also prints pandas df default index)

# test
end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken: {time_taken} seconds")