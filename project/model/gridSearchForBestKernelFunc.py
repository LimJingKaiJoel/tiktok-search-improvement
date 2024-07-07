from sklearn.model_selection import GridSearchCV, train_test_split, KFold
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd
import pickle
import time
from transformers import DistilBertTokenizer, DistilBertModel
import torch
from sklearn.decomposition import PCA

# Download necessary NLTK resources if needed
# nltk.download('wordnet')
# nltk.download('stopwords')

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

# Load pre-trained DistilBERT tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')

def tokenize_texts(texts, tokenizer, max_length=512):
    return tokenizer(
        list(texts),
        padding=True,
        truncation=True,
        return_tensors="pt",
        max_length=max_length
    )

# Tokenize the training and testing data
train_encodings = tokenize_texts(X_train, tokenizer)
test_encodings = tokenize_texts(X_test, tokenizer)

with torch.no_grad():
    train_outputs = model(**train_encodings)
    test_outputs = model(**test_encodings)

# Get the embeddings from the last hidden state
X_train_embeddings = train_outputs.last_hidden_state[:, 0, :].numpy()
X_test_embeddings = test_outputs.last_hidden_state[:, 0, :].numpy()

# Apply PCA to reduce dimensionality
pca = PCA(n_components=10)  # Adjust the number of components as needed
X_train_pca = pca.fit_transform(X_train_embeddings)
X_test_pca = pca.transform(X_test_embeddings)

param_grid = {
    'C': [1],
    'gamma': ['scale', 1],
    'kernel': ['rbf'],
    'class_weight': ['balanced']
}

# Initialize the GridSearchCV object
kf = KFold(n_splits=3, shuffle=True, random_state=42)  # Use fewer splits for faster computation
grid_search = GridSearchCV(SVC(random_state=42), param_grid, cv=kf, scoring='accuracy', n_jobs=-1)  # Use all available cores

print("Checkpoint")

# Fit GridSearchCV to the data
grid_search.fit(X_train_pca, y_train)

# Print the best parameters and best score
print("Best parameters found: ", grid_search.best_params_)
print("Best cross-validation score: ", grid_search.best_score_)

# Use the best estimator to make predictions
best_svm = grid_search.best_estimator_
y_pred_best_svm = best_svm.predict(X_test_pca)

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