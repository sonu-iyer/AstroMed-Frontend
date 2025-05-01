from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model and label encoders
with open("xgb_doctor_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("label_encoders.pkl", "rb") as f:
    label_encoders = pickle.load(f)

@app.route('/', methods=['POST'])
def predict():
    # Extract form data
    data = request.json  # Get data sent in JSON format

    # Map input data to required features
    features = [
        label_encoders['zodiac'].transform([data['zodiac']])[0],
        label_encoders['nakshatra'].transform([data['nakshatra']])[0],
        label_encoders['sunsign'].transform([data['sunsign']])[0],
        label_encoders['moonsign'].transform([data['moonsign']])[0],
        int(data['marsHouse']),
        int(data['merHouse']),
        int(data['jupHouse']),
        int(data['satHouse']),
        int(data['rahuHouse']),
        int(data['ketuHouse']),
    ]

    # Convert features into numpy array and reshape for model prediction
    features = np.array(features).reshape(1, -1)

    # Make prediction
    prediction = model.predict(features)

    # Return the result as JSON response
    result = {'prediction': 'Doctor' if prediction[0] == 1 else 'Not a Doctor'}
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
