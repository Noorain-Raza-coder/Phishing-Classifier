from src.components import data_ingestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException
import sys
import pandas as pd
import os

import pathlib
import sys, os
import numpy as np

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException


class TrainingPipeline:

    def start_data_ingestion(self):
        try:
            data_ingestion = DataIngestion()
            raw_data_dir = data_ingestion.initiate_data_ingestion()
            return raw_data_dir

        except Exception as e:
            raise CustomException(e, sys)



    def start_data_transformation(self, raw_data_file_path):
        try:
            file_name = "PhishingData.csv"
            full_file_path = os.path.join(raw_data_file_path , file_name)

            data_transformation = DataTransformation()
            x_train, x_test, y_train, y_test, preprocessor_path = data_transformation.initiate_data_transformation(full_file_path)
            return x_train, x_test, y_train, y_test, preprocessor_path

        except Exception as e:
            raise CustomException(e, sys)



    def start_model_training(self, x_train, x_test, y_train, y_test):
        try:
            model_trainer = ModelTrainer()
            model_trainer.initiate_model_training(x_train, x_test, y_train, y_test)

        except Exception as e:
            raise CustomException(e, sys)



    def run_pipeline(self):
        try:
            raw_data_dir = self.start_data_ingestion()
            x_train, x_test, y_train , y_test, preprocessor_path = self.start_data_transformation(raw_data_dir)
            self.start_model_training(x_train, x_test, y_train , y_test)

        except Exception as e:
            raise CustomException(e, sys)







if __name__ == '__main__':
    training_pipeline = TrainingPipeline()
    training_pipeline.run_pipeline()
    print("Training pipeline is done.")



