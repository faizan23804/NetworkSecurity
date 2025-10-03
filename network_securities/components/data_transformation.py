import pandas as pd
import numpy as np
import sys
import os

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_securities.constant.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS
from network_securities.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from network_securities.entity.config_entity import DataTransformationConfig
from network_securities.exceptions.exceptions import CustomException
from network_securities.logging.logger import logging
from network_securities.utils.main_utils import save_numpy_array_data,save_object


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise CustomException(e, sys)
        
        
    @staticmethod
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)
        

    def get_transformed_object(cls):
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step.

        Args:
          cls: DataTransformation

        Returns:
          A Pipeline object
        """
        logging.info(
            "Entered get_data_transformed_object method of Transformation class"
        )
        try:
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
            processor=Pipeline([("imputer",imputer)])
            return processor
        except Exception as e:
            raise CustomException(e, sys)
        
    def initiate_data_transformation(self):
        try:
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            #Train features
            X_train_features=train_df.drop(columns=[TARGET_COLUMN])
            y_train_feature=train_df[TARGET_COLUMN]
            y_train_feature=y_train_feature.replace(-1,0)

            #test features
            X_test_features=train_df.drop(columns=[TARGET_COLUMN])
            y_test_feature=train_df[TARGET_COLUMN]
            y_test_feature=y_test_feature.replace(-1,0)

            #Initiate Preprocessor(KNN-Imputer)
            preprocessor=self.get_transformed_object()

            #Fit and Transformation
            preprocessor_obj=preprocessor.fit(X_train_features)
            transformed_input_train_feature=preprocessor_obj.transform(X_train_features)
            transformed_input_test_feature=preprocessor_obj.transform(X_test_features)

            #Conversion to numpy array data
            train_arr=np.c_[transformed_input_train_feature,np.array(y_train_feature)]
            test_arr=np.c_[transformed_input_test_feature,np.array(y_test_feature)]

            #Save Numpy array data
            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr, )
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object( self.data_transformation_config.transformed_object_file_path, preprocessor_obj)

            save_object( "final_model/preprocessor.pkl", preprocessor_obj)

            #Data Transformation Artifacts
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact




        except Exception as e:
            raise CustomException(e, sys)
        