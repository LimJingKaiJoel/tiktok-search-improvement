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

# Train the SVM classifier with an RBF kernel
svm_rbf = SVC(kernel='rbf', gamma='scale', random_state=42)
svm_rbf.fit(X_train_tfidf, y_train)

# Predict on the test set using the RBF kernel SVM
y_pred_rbf = svm_rbf.predict(X_test_tfidf)

# Evaluate the RBF kernel SVM
print("\nRBF Kernel SVM")
print(classification_report(y_test, y_pred_rbf))
print(f'Accuracy: {accuracy_score(y_test, y_pred_rbf)}')

qn = "how do i win a hackathon"
nonqn = "beautiful sunset"

samples = [qn, nonqn]
samples_tfidf = vectorizer.transform(samples)

# nonlinear
sample_pred_rbf = svm_rbf.predict(samples_tfidf)
print("\nRBF Kernel SVM Predictions on Samples:")
for sample, pred in zip(samples, sample_pred_rbf):
    print(f'Sample: "{sample}" -> Prediction: {"Question" if pred == 1 else "Non-Question"}')

# Save the RBF SVM model
with open('svm_rbf_model.pkl', 'wb') as f:
    pickle.dump(svm_rbf, f)

# Save the vectorizer
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)