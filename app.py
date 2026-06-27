from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load trained model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:

        data = {
            "MedInc": [float(request.form["MedInc"])],
            "HouseAge": [float(request.form["HouseAge"])],
            "AveRooms": [float(request.form["AveRooms"])],
            "AveBedrms": [float(request.form["AveBedrms"])],
            "Population": [float(request.form["Population"])],
            "AveOccup": [float(request.form["AveOccup"])],
            "Latitude": [float(request.form["Latitude"])],
            "Longitude": [float(request.form["Longitude"])]
        }

        input_data = pd.DataFrame(data)

        prediction = model.predict(input_data)[0]

        estimated_price = prediction * 100000

        return render_template(
            "index.html",
            prediction_text=f"${estimated_price:,.2f}"
        )

    except Exception as e:

        return render_template(
            "index.html",
            prediction_text=f"Error: {e}"
        )


@app.route("/about")
def about():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)