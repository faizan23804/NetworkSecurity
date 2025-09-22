import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
import pymongo
from network_securities.exceptions.exceptions import CustomException
from network_securities.logging.logger import logging

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)


ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e, sys)
        
    def csv_to_json(self,file_path):
        try:
            dataset = pd.read_csv(file_path)
            dataset.reset_index(drop=True,inplace=True)
            records=list(json.loads(dataset.T.to_json()).values())
            return records

        except Exception as e:
            raise CustomException(e,sys)
        
    def insert_data_to_mongodb(self,records,database,collection):
        try:
            self.records=records
            self.database=database
            self.collection=collection

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)

            logging.info("Conversion to Json Successfull")

            return(len(self.records))
        except Exception as e:
            raise CustomException(e, sys)
        


if __name__=='__main__':
    try:
        FILE_PATH="Network_data\phisingData.csv"
        Database="NetworkSecurity"
        Collection="NetworkDataset"
        networkobj=NetworkDataExtract()
        records=networkobj.csv_to_json(file_path=FILE_PATH)
        #print(records)
        number_of_records=networkobj.insert_data_to_mongodb(records,Database,Collection)
        print(f"The Total Number of Records are: {number_of_records}")
        logging.info("Dataset Pushed to Mongo Database.")
    except Exception as e:
        raise CustomException(e, sys)

