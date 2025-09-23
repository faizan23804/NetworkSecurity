import pandas as pd
import numpy as np
import os
import sys


"""
Data Ingeestion related constant start with Data_Ingestion VAR name.
"""


DATA_INGESTION_COLLECTION_NAME:str = "NetworkDataset"
DATA_INGESTION_DATABASE_NAME:str = "NetworkSecurity"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.25

"""
Defining common constant variable for training pipeline

"""

TARGET_COLUMN:str = "Result"
PIPELINE_NAME:str = "NETWORK_SECURITY"
ARTIFACTS_DIR:str = "Artifacts"
FILE_NAME:str = "phishingData.csv"
TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"