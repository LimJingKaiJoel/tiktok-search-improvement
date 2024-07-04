from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    text: str

model_path = os.path.join(os.path.dirname(__file__), 'svm_rbf_model.pkl')
vectorizer_path = os.path.join(os.path.dirname(__file__), 'vectorizer.pkl')

def load_model():
    if not os.path.exists(model_path):
        raise HTTPException(status_code=500, detail="Model file not found")
    with open(model_path, 'rb') as f:
        model = joblib.load(f)
    return model

def load_vectorizer():
    if not os.path.exists(vectorizer_path):
        raise HTTPException(status_code=500, detail="Vectorizer file not found")
    with open(vectorizer_path, 'rb') as f:
        vectorizer = joblib.load(f)
    return vectorizer

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        text = request.text
        vectorizer = load_vectorizer()
        model = load_model()
        text_tfidf = vectorizer.transform([text])
        prediction = model.predict(text_tfidf)
        return {"prediction": "Question" if prediction[0] == 1 else "Non-Question"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

handler = Mangum(app)