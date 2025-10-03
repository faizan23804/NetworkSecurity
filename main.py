from network_securities.exceptions.exceptions import CustomException
from network_securities.logging.logger import logging

from network_securities.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from network_securities.entity.config_entity import TrainingPipelineConfig
from network_securities.components.data_ingestion import DataIngestion
from network_securities.components.data_validation import DataValidation
from network_securities.components.data_transformation import DataTransformation
import sys



if __name__=='__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        print(dataingestionartifact)
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        logging.info("Initiate the data Validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("data Validation Completed")
        print(data_validation_artifact)
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        logging.info("Initiate Data Transformation")
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        logging.info("Data Transformation Completed.")
        print(data_transformation_artifact)
        
    except  Exception as e:
        raise CustomException(e, sys)