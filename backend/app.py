import os
import numpy as np
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask_cors import CORS  # allow React to connect

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Load models once
mobilenet = load_model("models/best_model_mobilenetv2.h5")
efficientnet = load_model("models/best_model_b41.h5")

# Labels for classification
labels = ['A+', 'A-', 'AB+', 'AB-', 'B+', 'B-', 'O+', 'O-']

# Function to predict blood group
def predict_blood_group(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    pred1 = mobilenet.predict(img_array)
    pred2 = efficientnet.predict(img_array)
    final_pred = (pred1 + pred2) / 2
    predicted_label = labels[np.argmax(final_pred)]
    return predicted_label

@app.route("/", methods=["GET"])
def home():
    return "✅ Flask backend is up!"

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image file in request"})

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    # Save image to static folder
    if not os.path.exists("static"):
        os.makedirs("static")

    file_path = os.path.join("static", file.filename)
    file.save(file_path)

    # Predict
    prediction = predict_blood_group(file_path)
    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    app.run(debug=True)
