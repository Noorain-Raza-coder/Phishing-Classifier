from src.exception import CustomException
import sys
import os
import pickle
import boto3
from src.constant import *

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




def upload_file(from_filename, to_filename, bucket_name):
    try:
        s3_resource = boto3.resource("s3")

        s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)

    except Exception as e:
        raise CustomException(e, sys)


def download_model(bucket_name, bucket_file_name, destination_file_name):
    try:
        s3_client = boto3.client("s3")

        s3_client.download_file(bucket_name, bucket_file_name, destination_file_name)

        return destination_file_name

    except Exception as e:
        raise CustomException(e, sys)