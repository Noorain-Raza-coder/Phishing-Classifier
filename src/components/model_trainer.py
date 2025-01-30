from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier

from sklearn.metrics import accuracy_score , precision_score , recall_score
import pickle
import pandas as pd

from dataclasses import dataclass
import os
from src.logger import logging
from src.exception import CustomException
import sys
from src import utils
from src.constant import *




@dataclass
class ModelTrainerConfig:
    model_object_path = os.path.join("artifacts" , "model.pkl")


class ModelTrainer:
    def __init__(self) -> None:
        self.model_trainer_config =  ModelTrainerConfig()

        self.models = {
                        "GaussianNB": GaussianNB(),
                        "XGBClassifier": XGBClassifier(objective='binary:logistic'),
                        "LogisticRegression": LogisticRegression()
                    }

    

    def Model_Evaluation(self , model , x_train , x_test , y_train , y_test):
        try:
            model.fit(x_train,y_train)
            y_pred = model.predict(x_test)
            accur = accuracy_score(y_test , y_pred)
            prec = precision_score(y_test , y_pred)
            recal = recall_score(y_test , y_pred)
            
            return accur,prec,recal
        
        except Exception as e:
            raise CustomException(e,sys)


    
    def BestModel(self , models , x_train , x_test , y_train , y_test):
        model_name = []
        accu_score = []
        prec_score = []
        recal_score = []

        try:

            for model in self.models:
                accur,prec,recal = self.Model_Evaluation(models[model] , x_train , x_test , y_train , y_test)
                accu_score.append(accur)
                prec_score.append(prec)
                recal_score.append(recal)
                model_name.append(model)


            data = {"Models" : model_name , "Accuracy" : accu_score , "Precision" : prec_score, "Recall" : recal_score}
            df_scores = pd.DataFrame(data)
            model = df_scores.sort_values(by="Recall" , ascending=False).iloc[0]
            best_model = model[0]
            best_score = {"Accuracy" : model[1],"Precision" : model[2],"Recall" : model[3],}
            
            return best_model , best_score

        except Exception as e:
            raise CustomException(e,sys)



    def initiate_model_training(self , x_train , x_test , y_train , y_test):
        try:

            best_model , best_score = self.BestModel(self.models , x_train , x_test , y_train , y_test)

            print("\nBest Model : ",best_model)
            print("Best Score : ", best_score)

            final_model = self.models[best_model]

            final_model.fit(x_train , y_train)

            utils.save_obj(obj = final_model , file_path = self.model_trainer_config.model_object_path)

            utils.upload_file(from_filename=self.model_trainer_config.model_object_path,
                                   to_filename="model.pkl",
                                   bucket_name=AWS_S3_BUCKET_NAME)
        
        except Exception as e:
            raise CustomException(e,sys)

        

        
