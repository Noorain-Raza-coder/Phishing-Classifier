from flask import Flask, render_template, jsonify, request, send_file
from src.exception import CustomException
from src.logger import logging
import os,sys

from src.pipelines.training_pipeline import TrainingPipeline
from src.pipelines.prediction_pipeline import PredictionPipeline

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('prediction.html')



@app.route('/predict', methods=['POST', 'GET'])
def predict():
    
    try:
        if request.method == 'POST':
            prediction_pipeline = PredictionPipeline(request)
            prediction = prediction_pipeline.initiate_prediction_pipeline()
            if prediction[0] == 0:
                output = "Phishing"
            else :
                output = "Safe"

            return render_template('prediction.html' , prediction=output)

            # logging.info("prediction completed. Downloading prediction file.")
            # return send_file(prediction_file_detail.prediction_file_path,
            #                 download_name= prediction_file_detail.prediction_file_name,
            #                 as_attachment= True)
        
        else:
            return render_template('prediction.html')

    except Exception as e:
        raise CustomException(e,sys)
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug= True)