import os
import logging
import boto3
import json
from botocore.client import Config
from botocore.exceptions import ClientError
import time

region_name = "cn-north-1"

# os.environ["http_proxy"] = 'http://localhost'
# os.environ["https_proxy"] = 'https://localhost'

logger = logging.getLogger()
boto3.set_stream_logger('', level=logging.INFO)

config = Config(proxies={})


def get_secret_from_secretsmanager():
    # print(config)
    secret_name = "gaksk"
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name,
        config=config
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        # raise e
        return

    # Decrypts secret using the associated KMS key.
    secret = json.loads(get_secret_value_response['SecretString'])
    ak, sk = secret.get('gak'), secret.get('gsk')
    return ak, sk


get_secret_from_secretsmanager()
