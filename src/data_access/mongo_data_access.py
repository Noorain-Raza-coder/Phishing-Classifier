from src.exception import CustomException
import os
import sys
import pandas as pd
import numpy as np
from pymongo import MongoClient
from typing import List, Generator

from dotenv import load_dotenv
load_dotenv()



class GetData:
    """
    This class helps to export entire MongoDB records as a Pandas DataFrame.
    """

    def __init__(self, database_name: str):
        try:
            self.database_name = database_name
            self.mongo_url = os.getenv("MONGO_DB_URL")

            # Establish MongoDB connection
            self.client = MongoClient(self.mongo_url)
            self.database = self.client[self.database_name]

        except Exception as e:
            raise CustomException("Error initializing MongoDB connection", e)

    def get_collection_names(self) -> List[str]:
        """
        Retrieves the names of all collections in the database.
        """
        try:
            return self.database.list_collection_names()
        except Exception as e:
            raise CustomException("Error fetching collection names", e)

    def get_collection_data(self, collection_name: str) -> pd.DataFrame:
        """
        Retrieves all documents from a given collection and returns a Pandas DataFrame.
        """
        try:
            collection = self.database[collection_name]
            data = list(collection.find({}))  # Fetch all documents

            if not data:  # If collection is empty, return an empty DataFrame
                return pd.DataFrame()

            df = pd.DataFrame(data)

            # Drop MongoDB "_id" field if it exists
            if "_id" in df.columns:
                df = df.drop(columns=["_id"])

            # Replace "na" with NaN
            df = df.replace({"na": np.nan})

            return df

        except Exception as e:
            raise CustomException(f"Error fetching data from collection: {collection_name}", e)

    def export_collections_as_dataframe(self) -> Generator:
        """
        Generator function to export all collections as Pandas DataFrames.
        """
        try:
            collections = self.get_collection_names()
            for collection_name in collections:
                df = self.get_collection_data(collection_name)
                yield collection_name, df

        except Exception as e:
            raise CustomException("Error exporting collections", e)
