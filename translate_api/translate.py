import logging
import os
import boto3
from flask import Flask, request, jsonify

app = Flask(__name__)

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
        data = request.args

        # Use provided ak/sk or fallback to environment variable
        ak = data.get('ak', default_ak)
        sk = data.get('sk', default_sk)

        # If both are still None, return an error
        if not ak or not sk:
            return jsonify(error="Missing AWS credentials"), 400

        source_language = data.get('src', 'en')
        destination_language = data.get('dst', 'zh')
        message = data.get('msg', 'this a test message')

        global client
        client = boto3.client('translate', region_name=region, aws_access_key_id=ak, aws_secret_access_key=sk)

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=10000)
