from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import pickle
import time
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

param_grid = {
    'C': [0.1, 1, 10],
    'gamma': ['scale', 'auto', 0.01, 0.1, 1, 10],
    'kernel': ['rbf'],
    'class_weight': ['balanced']  # Add this parameter to handle class imbalance
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

# Save the best model
with open('best_svm_model.pkl', 'wb') as f:
    pickle.dump(best_svm, f)

end_time = time.time()
time_taken = end_time - start_time
print(f"Time taken: {time_taken} seconds")

# # Define the parameter grid
# param_distributions = {
#     'C': [0.1, 1, 10],
#     'gamma': ['scale', 0.1, 1],
#     'kernel': ['rbf', 'poly', 'sigmoid']
# }

# # Generating a synthetic imbalanced dataset
# X, y = make_classification(n_samples=30000, n_features=20, n_classes=2, weights=[0.67, 0.33])

# # Splitting the dataset
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Initialize the SVM model
# svm = SVC(class_weight='balanced')

# # Initialize RandomizedSearchCV
# random_search = RandomizedSearchCV(estimator=svm, param_distributions=param_distributions, n_iter=10, cv=3, verbose=1, n_jobs=-1, random_state=42)

# # Fit RandomizedSearchCV
# random_search.fit(X_train, y_train)

# # Predicting and evaluating
# y_pred = random_search.best_estimator_.predict(X_test)
# print(classification_report(y_test, y_pred))

# Define the parameter grid for SVM
