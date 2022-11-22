import os
import boto3
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# read ak/sk from env
print(os.environ.get('ak'))
print(os.environ.get('sk'))


@app.route('/translate', methods=['post', 'get'])
def translate():
    """
    require: msg
    :return:
    """
    try:
        data = request.args
        # get aws ak and sk
        ak, sk = os.environ.get('ak'), os.environ.get('sk')
        region = os.environ.get('region', 'us-east-1')
        # and source_language and destination_language, for default, source_language = 'en', destination_language = 'zh'
        source_language, destination_language = data.get('src', 'en'), data.get('dst', 'zh')
        message = data.get('msg', 'this a test message')

        client = boto3.client('translate', region_name=region, aws_access_key_id=ak, aws_secret_access_key=sk)

        response = client.translate_text(
            Text=message,
            SourceLanguageCode=source_language,
            TargetLanguageCode=destination_language,
        )
        print(response)

    except Exception as e:
        print(e)

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


app.run(port=8888, host='0.0.0.0', debug=True)
