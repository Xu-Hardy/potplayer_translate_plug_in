import logging
import os
import boto3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 这将为您的整个应用启用CORS

# Set default from environment variables
default_ak = os.environ.get('aws_access_key_id')
default_sk = os.environ.get('aws_secret_access_key')
region = os.environ.get('region', 'us-east-1')
client = boto3.client('translate', region_name=region, aws_access_key_id=default_ak, aws_secret_access_key=default_sk)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/')
def home():
    return {
        'health check': 'pass'
    }


@app.route('/translate', methods=['POST', 'GET'])
def translate():
    try:
        data = request.json
        print(data)

        source_language = data.get('src', 'en')
        destination_language = data.get('dst', 'zh')
        message = data.get('msg', 'this a test message')

        response = client.translate_text(
            Text=message,
            SourceLanguageCode=source_language,
            TargetLanguageCode=destination_language,
        )

        logger.info(response)
        return jsonify(
            from_language=source_language,
            to_language=destination_language,
            trans_result=[
                {
                    "src": message,
                    "dst": response.get('TranslatedText', "No translation available")
                }
            ]
        )
    except Exception as e:
        logger.error(f"Error translating text: {e}")
        return jsonify(error=str(e)), 500


@app.route('/pt', methods=['post', 'get'])
def translate_pt():
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
    # ak = data.get('ak', 'this a test message') sk = data.get('sk', 'this a test message') global client if client
    # is None: client = boto3.client('translate', region_name=region, aws_access_key_id=ak, aws_secret_access_key=sk)
    # if ak is not None and sk is not None else None

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
    app.run(host='0.0.0.0', debug=True, port=50000)
