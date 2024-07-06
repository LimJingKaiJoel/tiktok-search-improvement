from sklearn.model_selection import GridSearchCV
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import pickle


# Load the data
questions_csv_file_path = 'https://raw.githubusercontent.com/LimJingKaiJoel/tiktok-search-improvement/main/project/identifying%20questions/TrainingDataQuestions.csv'
non_questions_csv_file_path = 'https://raw.githubusercontent.com/LimJingKaiJoel/tiktok-search-improvement/main/project/identifying%20questions/TrainingDataNonQuestions.csv'

# Load questions from the first CSV
df_questions = pd.read_csv(questions_csv_file_path)
questions = df_questions['question'].dropna().tolist()

# Load non-questions from the second CSV
df_non_questions = pd.read_csv(non_questions_csv_file_path)
non_questions = df_non_questions['non question'].dropna().tolist()

# Prepare the data
data = pd.DataFrame({
    'text': questions + non_questions,
    'label': [1] * len(questions) + [0] * len(non_questions)
})
X_train, X_test, y_train, y_test = train_test_split(data['text'], data['label'], test_size=0.2, random_state=42)

# tfidf to convert words to vector embedding space
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Define the parameter grid for SVM
param_grid = {
    'C': [0.1, 1, 10],
    'gamma': ['scale', 0.1, 1],
    'kernel': ['rbf', 'poly', 'sigmoid']
}

# Initialize the GridSearchCV object
grid_search = GridSearchCV(SVC(random_state=42), param_grid, cv=5, scoring='accuracy')

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