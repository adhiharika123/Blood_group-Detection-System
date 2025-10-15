import React, { useState } from "react";
import "./App.css";

function App() {
  const [image, setImage] = useState(null);
  const [prediction, setPrediction] = useState("");
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e) => {
    setImage(e.target.files[0]);
    setPrediction("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) {
      alert("Please upload an image first");
      return;
    }

    const formData = new FormData();
    formData.append("image", image);

    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setPrediction(data.prediction);
    } catch (err) {
      console.error("Error:", err);
      alert("Failed to connect to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>🩸 Blood Group Prediction</h1>

      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleImageChange} />
        <br />
        <button type="submit">Predict</button>
      </form>

      {loading && <p className="result">⏳ Predicting...</p>}
      {prediction && (
        <p className="result">
          ✅ Predicted Blood Group: <strong>{prediction}</strong>
        </p>
      )}
    </div>
  );
}

export default App;
