
from flask import Flask, render_template, request
import joblib

# Load model and vectorizer
model = joblib.load("fake_news_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    if request.method == "POST":
        news_text = request.form["news_text"]
        vector = vectorizer.transform([news_text])
        pred = model.predict(vector)[0]
        prediction = "REAL" if pred == "REAL" else "FAKE"
    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
