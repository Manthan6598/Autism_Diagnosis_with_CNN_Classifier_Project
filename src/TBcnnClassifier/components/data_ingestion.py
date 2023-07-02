import os
import urllib.request as request
import zipfile
from TBcnnClassifier import logger
from TBcnnClassifier.utils.common import get_size
import boto3
from TBcnnClassifier.entity.config_entity import DataIngestionConfig
from pathlib import Path

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        session = boto3.resource(
            service_name='s3',
            region_name='eu-north-1',
            aws_access_key_id='AKIAWLYTVYE57LST7NEW',
            aws_secret_access_key='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'
        )
        self.s3_client = session.meta.client

    
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            bucket_name = 'autisticdatabucket'
            object_key = 'consolidated.zip'
            self.s3_client.download_file(bucket_name, object_key, self.config.local_data_file)
            logger.info(f"File downloaded from S3 bucket: {self.config.local_data_file}")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")

    
    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)

