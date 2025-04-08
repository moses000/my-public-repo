import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import numpy as np

# Load and preprocess dataset (simulation for real-time data)
data = pd.read_csv('network_fault_data.csv')

# Simulate real-time data by adding noise or fetching from an API
def simulate_realtime_data():
    features = np.random.rand(3)  # Simulated features
    return features

# Feature engineering (example)
X = data[['feature1', 'feature2', 'feature3']]  # Replace with actual feature columns
y = data['fault']  # Target variable (fault or no fault)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the trained model
joblib.dump(model, 'fault_prediction_model.pkl')

# Real-time prediction loop (optional)
while True:
    features = simulate_realtime_data()
    print(f"Predicted fault status: {model.predict([features])[0]}")
    time.sleep(1)  # Simulate delay between predictions
