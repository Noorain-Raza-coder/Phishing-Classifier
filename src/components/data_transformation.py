import sys
import os
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from imblearn.over_sampling import RandomOverSampler

from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass

from src import utils


@dataclass
class DataTransformationConfig:
    preprocessor_obj_path = os.path.join("artifacts","preprocessor.pkl")
    


class DataTransformation:
    def __init__(self) -> None:
        self.data_transformation_config = DataTransformationConfig()


    

    def initiate_data_transformation(self , raw_data_file_path):
        """
            Method Name :   initiate_data_transformation
            Description :   This method initiates the data transformation component for the pipeline 
            
            Output      :   data transformation artifact is created and returned 
            On Failure  :   Write an exception log and then raise an exception
            
            Version     :   1.2
            Revisions   :   moved setup to cloud
        """

        logging.info(
            "Entered initiate_data_transformation method of Data_Transformation class"
        )

        try:
            df = pd.read_csv(raw_data_file_path)

            TARGET_COLUMN = 'CLASS_LABEL'
            drop_columns = ['id' , TARGET_COLUMN]

            ## splitting independent and target variable
            x = df.drop(columns=drop_columns, axis=1)
            y = df[TARGET_COLUMN]

            sampler = RandomOverSampler()
            x_sampled, y_sampled = sampler.fit_resample(x, y)

            X_train, X_test, y_train, y_test = train_test_split(x_sampled, y_sampled, test_size=0.2)

            preprocessor = SimpleImputer(strategy='most_frequent')

            x_train_scaled = preprocessor.fit_transform(X_train)
            x_test_scaled = preprocessor.transform(X_test)

            preprocessor_path = self.data_transformation_config.preprocessor_obj_path

            os.makedirs(os.path.dirname(preprocessor_path), exist_ok=True)
            utils.save_obj(obj=preprocessor , file_path=preprocessor_path)

            return x_train_scaled, x_test_scaled, y_train, y_test, preprocessor_path

        except Exception as e:
            raise CustomException(e, sys)