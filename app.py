
from flask import Flask, render_template, request
import joblib
import os

app = Flask(__name__)

# Debug: Check files
print("Available files:", [f for f in os.listdir('.') if f.endswith(('.pkl', '.gli'))])

# Load models
try:
    # Try .pkl first, then .gli
    if os.path.exists("fake_news_model.pkl"):
        model = joblib.load("fake_news_model.pkl")
        vectorizer = joblib.load("vectorizer.pkl")
    elif os.path.exists("fake_news_model.gli"):
        model = joblib.load("fake_news_model.gli")
        vectorizer = joblib.load("vectorizer.gli")
    else:
        raise FileNotFoundError("No model files found (.pkl or .gli)")
    
    print("✅ Models loaded successfully!")
    models_loaded = True
    
except Exception as e:
    print(f"❌ Error loading models: {e}")
    models_loaded = False

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    if request.method == "POST":
        if not models_loaded:
            prediction = "Error: AI models not loaded. Please check server logs."
        else:
            news_text = request.form.get("news_text", "").strip()
            if not news_text:
                prediction = "Please enter some text to analyze."
            else:
                try:
                    vector = vectorizer.transform([news_text])
                    pred = model.predict(vector)[0]
                    prediction = "REAL" if pred == "REAL" else "FAKE"
                except Exception as e:
                    prediction = f"Analysis error: {str(e)}"
    
    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)