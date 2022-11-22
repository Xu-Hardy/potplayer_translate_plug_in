import boto3
from flask import Flask, request

app = Flask(__name__)


@app.route('/translate', methods=['post', 'get'])
def translate():
    try:
        data = request.args
        # get aws ak and sk
        ak, sk = data.get('ak'), data.get('sk')
        # and source_lanuage and destination_lanuage, source_lanuage = 'en', destination_lanuage = 'zh'
        source_language, destination_language = data.get('src', 'en'), data.get('dst', 'zh')
        message = data.get('msg', 'this a test message')

        client = boto3.client('translate', region_name=ak, aws_access_key_id=sk)

        response = client.translate_text(
            Text=message,
            SourceLanguageCode=source_language,
            TargetLanguageCode=destination_language,
        )
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
