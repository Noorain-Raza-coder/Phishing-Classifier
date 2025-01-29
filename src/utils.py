from src.exception import CustomException
import sys
import os
import pickle

def save_obj(obj , file_path):
    try :
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path , exist_ok=True)

        with open(file_path , 'wb') as file_obj:
            pickle.dump(obj , file_obj)

    except Exception as e:
        raise CustomException(e,sys)



def load_obj(obj_path):
    try :
        with open(obj_path, 'rb') as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        raise CustomException(e,sys)
