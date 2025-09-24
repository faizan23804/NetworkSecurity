from network_securities.exceptions.exceptions import CustomException
from network_securities.logging.logger import logging

from network_securities.entity.config_entity import DataIngestionConfig
from network_securities.entity.artifact_entity import DataIngestionArtifact
import pandas as pd
import numpy as np
import os
import sys
import pymongo
from sklearn.model_selection import train_test_split
from typing import List


from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys)
        
    def export_collection_as_dataframe(self):
        """
        Read The Json file from mongo db and convert to csv.
        """
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]

            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop(columns=["_id"],inplace=True,axis=1)
            df.replace({'na':np.nan},inplace=True)
            logging.info("DataFrame Created Succesfully.")
            return df    

        except Exception as e:
            raise CustomException(e, sys)
        

    def export_data_into_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_path=self.data_ingestion_config.feature_store_file_path

            dir_path=os.path.dirname(feature_path)
            os.makedirs(dir_path,exist_ok=True)

            dataframe.to_csv(feature_path,header=True,index=False)
            logging.info("DataFrame Exported Succesfully.")
            return dataframe
        except Exception as e:
            raise CustomException(e, sys)
        
    def data_train_test_split(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Train and Test Split Succesfull")

            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_set.to_csv(self.data_ingestion_config.training_file_path, header=True,index=False)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, header=True,index=False)

            logging.info("Train set and Test set Exported")

        except Exception as e:
            raise CustomException(e, sys)
        

    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.data_train_test_split(dataframe)
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact
        except Exception as e:
            raise CustomException(e,sys)

