from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)
model = load_model("Obesity Predictor/obesity_ann_model.keras")
scaler = joblib.load("Obesity Predictor/obesity_scaler.pkl")
feature_encoders = joblib.load("Obesity Predictor/feature_encoders.pkl")
target_encoder = joblib.load("Obesity Predictor/target_encoder.pkl")


feature_columns = [
    'Age',
    'Gender',
    'Height',
    'Weight',
    'CALC',
    'FAVC',
    'FCVC',
    'NCP',
    'SCC',
    'SMOKE',
    'CH2O',
    'family_history_with_overweight',
    'FAF',
    'TUE',
    'CAEC',
    'MTRANS'
]



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        input_data = {
            "Age": float(data["Age"]),
            "Gender": data["Gender"],
            "Height": float(data["Height"]),
            "Weight": float(data["Weight"]),
            "CALC": data["CALC"],
            "FAVC": data["FAVC"],
            "FCVC": float(data["FCVC"]),
            "NCP": float(data["NCP"]),
            "SCC": data["SCC"],
            "SMOKE": data["SMOKE"],
            "CH2O": float(data["CH2O"]),
            "family_history_with_overweight":
                data["family_history_with_overweight"],
            "FAF": float(data["FAF"]),
            "TUE": float(data["TUE"]),
            "CAEC": data["CAEC"],
            "MTRANS": data["MTRANS"]
        }

    
        for column, encoder in feature_encoders.items():

            if column in input_data:

                input_data[column] = encoder.transform(
                    [input_data[column]]
                )[0]

        df = pd.DataFrame(
            [[input_data[col] for col in feature_columns]],
            columns=feature_columns)
        
        scaled_data = scaler.transform(df)
        prediction_prob = model.predict(scaled_data,verbose=0)
        

        predicted_class_index = np.argmax(prediction_prob,axis=1)[0]

        confidence = float(
            np.max(prediction_prob) * 100)
    

        prediction = target_encoder.inverse_transform(
            [predicted_class_index])[0]

        if prediction == "Normal_Weight":
            badge = "Healthy"

        elif prediction in [
            "Overweight_Level_I",
            "Overweight_Level_II"
        ]:
            badge = "Warning"

        else:
            badge = "Risk"

        return jsonify({
            "prediction": prediction.replace("_", " "),
            "confidence": round(confidence, 2),
            "status": badge
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        debug=True)
    