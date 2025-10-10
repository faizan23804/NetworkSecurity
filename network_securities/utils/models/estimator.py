from network_securities.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
from network_securities.exceptions.exceptions import CustomException
from network_securities.logging.logger import logging
import os
import sys

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as e:
            raise CustomException(e,sys)
        
    def predict(self,x):
        try:
            x_transform=self.preprocessor.transform(x)
            y_hat=self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise CustomException(e,sys)
        