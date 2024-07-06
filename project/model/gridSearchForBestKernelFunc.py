from sklearn.model_selection import GridSearchCV, train_test_split, KFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import pickle
import time
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

start_time = time.time()

# Load the data
questions_csv_file_path = 'https://raw.githubusercontent.com/LimJingKaiJoel/tiktok-search-improvement/main/project/identifying%20questions/TrainingDataQuestions.csv'
non_questions_csv_file_path = 'https://raw.githubusercontent.com/LimJingKaiJoel/tiktok-search-improvement/main/project/identifying%20questions/TrainingDataNonQuestions.csv'

# Load questions from the first CSV
df_questions = pd.read_csv(questions_csv_file_path)
questions = df_questions['question'].dropna().tolist()

# Load non-questions from the second CSV
df_non_questions = pd.read_csv(non_questions_csv_file_path)
non_questions = df_non_questions['non question'].dropna().tolist()

# Preprocess the data
questions = [preprocess_text(q) for q in questions]
non_questions = [preprocess_text(nq) for nq in non_questions]

# Prepare the data
data = pd.DataFrame({
    'text': questions + non_questions,
    'label': [1] * len(questions) + [0] * len(non_questions)
})
X_train, X_test, y_train, y_test = train_test_split(data['text'], data['label'], test_size=0.2, random_state=42)

# tfidf to convert words to vector embedding space
vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Save the fitted TF-IDF vectorizer
with open('tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

param_grid = {
    'C': [0.1, 1, 10],
    'gamma': ['scale', 'auto', 0.01, 0.1, 1, 10],
    'kernel': ['rbf'],
    'class_weight': ['balanced']
}

# Initialize the GridSearchCV object
kf = KFold(n_splits=5, shuffle=True, random_state=42)
grid_search = GridSearchCV(SVC(random_state=42), param_grid, cv=kf, scoring='accuracy')

# Fit GridSearchCV to the data
grid_search.fit(X_train_tfidf, y_train)

# Print the best parameters and best score
print("Best parameters found: ", grid_search.best_params_)
print("Best cross-validation score: ", grid_search.best_score_)

# Use the best estimator to make predictions
best_svm = grid_search.best_estimator_
y_pred_best_svm = best_svm.predict(X_test_tfidf)

# Evaluate the best estimator
print("\nBest SVM Model")
print(classification_report(y_test, y_pred_best_svm))
print(f'Accuracy: {accuracy_score(y_test, y_pred_best_svm)}')

# Save the best model
with open('best_svm_model.pkl', 'wb') as f:
    pickle.dump(best_svm, f)

end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken: {time_taken} seconds")
