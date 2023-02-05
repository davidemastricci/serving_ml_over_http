from flask import Flask, request, jsonify
from flask.logging import create_logger
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import logging

app = Flask(__name__)
log = create_logger(app)
log.setLevel(logging.INFO)


def scale(payload):
    # here should be used the same scaler used for training
    log.info(f"Scaling payload: {payload} payload")
    scaler = StandardScaler().fit(payload)
    return scaler.transform(payload)


@app.route('/')
def index():
    return 'Hello, World!'


@app.route("/predict", methods=['POST'])
def predict():
    """
    Input Sample:
        {
            "CHAS": { "0": 0 }, "RM": { "0": 6.575 },
            "TAX": { "0": 296 }, "PTRATIO": { "0": 15.3 },
            "B": { "0": 396.9 }, "LSTAT": { "0": 4.98 }
        }

    Output Sample:
        { "prediction": [19.8479940652156348]}
    """
    json_payload = request.json
    try:
        clf = joblib.load("boston_housing_prediction.joblib")
    except Exception:
        log.info(f"JSON payload: \
        {json_payload} json payload")
    inference_payload = pd.DataFrame(json_payload)
    log.info(f"inference payload DataFrame: \
        {inference_payload} inference_payload")
    scaled_payload = scale(inference_payload)
    prediction = list(clf.predict(scaled_payload))
    return jsonify({"prediction": prediction})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
