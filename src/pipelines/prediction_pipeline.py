from src.exception import CustomException
from src.logger import logging
import sys
import os
from src import utils
import pandas as pd
from flask import request
from dataclasses import dataclass
from src.constant import *
        



class PredictionPipeline:
    def __init__(self, request: request):

        self.request = request
        



    def save_input_files(self)-> str:

        """
            Method Name :   save_input_files
            Description :   This method saves the input file to the prediction artifacts directory. 
            
            Output      :   input dataframe
            On Failure  :   Write an exception log and then raise an exception
            
            Version     :   1.2
            Revisions   :   moved setup to cloud
        """

        try:
            test_data_dir = "test_csv_data"
            os.makedirs(test_data_dir, exist_ok=True)

            input_csv_file = self.request.files['file']
            test_data_file_path = os.path.join(test_data_dir, input_csv_file.filename)
            
            input_csv_file.save(test_data_file_path)

            return test_data_file_path

        except Exception as e:
            raise CustomException(e,sys)


    def predict(self, features):
            try:

                # preprocessor_obj_path = os.path.join("artifacts" , "preprocessor.pkl")
                # model_obj_path = os.path.join("artifacts" , "model.pkl")

                # preprocessor = utils.load_obj(preprocessor_obj_path)
                # model = utils.load_obj(model_obj_path)

                model_path = utils.download_model(
                    bucket_name=AWS_S3_BUCKET_NAME,
                    bucket_file_name="model.pkl",
                    destination_file_name="model.pkl",
                )

                model = utils.load_obj(obj_path=model_path)

                preds = model.predict(features)

                return preds

            except Exception as e:
                raise CustomException(e, sys)
        
    def get_predicted_dataframe(self, test_data_file_path:pd.DataFrame):

        """
            Method Name :   get_predicted_dataframe
            Description :   this method returns the dataframw with a new column containing predictions

            
            Output      :   predicted dataframe
            On Failure  :   Write an exception log and then raise an exception
            
            Version     :   1.2
            Revisions   :   moved setup to cloud
        """
   
        try:

            test_df: pd.DataFrame = pd.read_csv(test_data_file_path)
            
            predictions = self.predict(test_df)
            return predictions
            



        except Exception as e:
            raise CustomException(e, sys)
        

        
    def initiate_prediction_pipeline(self):
        try:
            test_data_csv_path = self.save_input_files()
            prediction = self.get_predicted_dataframe(test_data_csv_path)

            return prediction


        except Exception as e:
            raise CustomException(e,sys)
            
        

 
        

        