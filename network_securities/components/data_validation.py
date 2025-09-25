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