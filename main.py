from networksequrity.entity.config_entity import TrainingPipelineConfig
from networksequrity.entity.config_entity import DataIngestionConfig

from networksequrity.components.data_ingestion import DataIngestion
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
        
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)
