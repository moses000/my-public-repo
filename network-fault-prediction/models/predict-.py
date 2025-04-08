import json
import joblib
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load pre-trained model
model = joblib.load('fault_prediction_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    features = list(data['network_data'].values())  # Adjust to handle your actual data structure
    
    # Predict fault (1 = Fault, 0 = No Fault)
    prediction = model.predict([features])
    
    # Return prediction result
    return jsonify({'prediction': str(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)  # Allow external access to Flask API
