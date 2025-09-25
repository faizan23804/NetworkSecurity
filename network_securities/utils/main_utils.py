import yaml
import dill
import pickle
from network_securities.exceptions.exceptions import CustomException
from network_securities.logging.logger import logging
import os
import sys

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e,sys)