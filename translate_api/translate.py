import logging
import os
import boto3
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# read ak/sk from env
ak, sk = os.environ.get('aws_access_key_id'), os.environ.get('aws_secret_access_key')

region = os.environ.get('region', 'us-east-1')
client = boto3.client('translate', region_name=region, aws_access_key_id=ak, aws_secret_access_key=sk)
logger = logging.getLogger()
boto3.set_stream_logger('', level=logging.DEBUG)


@app.route('/')
def home():
    return {
        'heath check': 'pass'
    }


@app.route('/translate', methods=['post', 'get'])
def translate():
    """
    require: msg
    :return:
    """
    # try:
    data = request.args
    # get aws ak and sk
    # and source_language and destination_language, for default, source_language = 'en', destination_language = 'zh'
    source_language, destination_language = data.get('src', 'en'), data.get('dst', 'zh')
    message = data.get('msg', 'this a test message')

    response = client.translate_text(
        Text=message,
        SourceLanguageCode=source_language,
        TargetLanguageCode=destination_language,
    )
    print(response)

    return {
        "from": f"{source_language}",
        "to": f"{destination_language}",
        "trans_result": [
            {
                "src": message,
                "dst": response.get('TranslatedText', "no message pls check script")
            }
        ]
    }


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
