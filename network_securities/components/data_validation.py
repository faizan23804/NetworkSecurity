from network_securities.exceptions.exceptions import CustomException
from network_securities.logging.logger import logging

from network_securities.entity.config_entity import DataIngestionConfig, DataValidationConfig
from network_securities.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from network_securities.constant.training_pipeline import SCHEMA_FILE_PATH
from network_securities.utils.main_utils import read_yaml_file

import os
import sys
import pandas as pd
from scipy.stats import ks_2samp


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact, data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        
        except Exception as e:
            raise CustomException(e, sys)
        

    @staticmethod
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)
        
    
    def validate_nos_of_columns(self,dataframe:pd.DataFrame):
        try:
            number_of_columns=len(self._schema_config)
            logging.info(f"Required number of columns:{number_of_columns}")
            logging.info(f"Data frame has columns:{len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_columns:
                return True
            else:
                return False

        except Exception as e:
            raise CustomException(e,sys)
        

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05):
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                distribution=ks_2samp(d1,d2)
                if threshold<=distribution.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{
                    "p_value":float(distribution.pvalue),
                    "drift_status":is_found
                    
                    }})
                
                drift_report_file_path = self.data_validation_config.drift_report_file_path

            #Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)

        except Exception as e:
            raise CustomException(e, sys)


        
    def initiate_data_validation(self):

        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            #Read Data from csv
            train_df=DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            #Validation of Columns
            status=self.validate_nos_of_columns(dataframe=train_df)
            if not status:
                error_message="Train dataframe does not contain all columns. \n"
            status=self.validate_nos_of_columns(dataframe=test_df)
            if not status:
                error_message="Test Dataframe does not contain all columns. \n"

            #Checking Drifting of Data
            status=self.detect_dataset_drift
        except Exception as e:
            raise CustomException(e, sys)