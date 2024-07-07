import pickle
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK resources
nltk.download('wordnet')
nltk.download('stopwords')

# Define a function to preprocess text
def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stopwords.words('english')]
    return ' '.join(words)

# Load the saved model
with open('best_svm_model.pkl', 'rb') as f:
    best_svm = pickle.load(f)

# Load the saved TF-IDF vectorizer
with open('distilbert_vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Function to predict if a query is a question
def predict_query(queries):
    preprocessed_queries = [preprocess_text(query) for query in queries]
    queries_tfidf = vectorizer.transform(preprocessed_queries)
    predictions = best_svm.predict(queries_tfidf)
    return predictions

# Sample input queries
input_queries = [
    "What is the tallest mountain in the world?",
    "Eliza Fletcher Memphis",
    "How does photosynthesis work?",
    "Juventus vs Real Madrid",
    "Where is the Eiffel Tower located?",
    "how do i win a hackathon",
    "In what country is Normandy located"
]

# Get predictions
predictions = predict_query(input_queries)

# Output the results
results = pd.DataFrame({
    'Query': input_queries,
    'Is Question': predictions
})

print(results)
