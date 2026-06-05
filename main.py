from networksequrity.entity.config_entity import TrainingPipelineConfig
from networksequrity.entity.config_entity import DataIngestionConfig,DataValidationConfig

from networksequrity.components.data_ingestion import DataIngestion
from networksequrity.components.data_validation import DataValidation
from networksequrity.logging.logger import logging
from networksequrity.exception.exception import NetworkSecurityException

import sys

if __name__=="__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        dataingestion = DataIngestion(dataingestionconfig)
        logging.info("Initiate Data Ingestion")
        dataingestionartifact = dataingestion.initiate_data_ingestion() 
        print(dataingestionartifact)
        logging.info('Data Initiation completed')
        logging.info("Initiate Data Validation")
        datavalidationconfig = DataValidationConfig(trainingpipelineconfig)
        datavalidation = DataValidation(dataingestionartifact,datavalidationconfig)
        
        data_validation_artifact = datavalidation.initiate_data_validation()
        logging.info("Data validation completed")
        print(data_validation_artifact)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)
