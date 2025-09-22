from fastapi import FastAPI, Request
import joblib
import logging

# Load your model
model = joblib.load("model.pkl")

# Configure logging
logging.basicConfig(
    filename="predictions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

@app.post("/predict")
async def predict(data: dict):
    area = data.get("area")
    
    # Handle invalid input
    if area is None:
        logging.error(f"Bad data received: {data}")
        return {"error": "Missing 'area' field"}

    try:
        pred = model.predict([[area]])[0]
        logging.info(f"Prediction request: {data}, Prediction: {pred}")
        return {"prediction": pred}
    except Exception as e:
        logging.error(f"Prediction failed for {data}. Error: {str(e)}")
        return {"error": "Prediction failed"}