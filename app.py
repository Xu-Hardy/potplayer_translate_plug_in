import boto3
from flask import Flask, request


server=Flask(__name__)

ak,sk='',''
client = boto3.client('translate',region_name=ak, aws_access_key_id=sk)

@server.route('/translate',methods=['post','get'])
def translate():

    data = request.args
    # source_lanuage = 'en'
    # destination_lanuage = 'zh'
    source_lanuage = data.get('src')
    destination_lanuage = data.get('dst')
    message = data.get('msg') 

    response=client.translate_text(
        Text=message,
        SourceLanguageCode=source_lanuage,
        TargetLanguageCode=destination_lanuage,
    )


    return {
        "from": f"{source_lanuage}",
        "to": f"{destination_lanuage}",
        "trans_result": [
        {
            "src": message,
            "dst": response['TranslatedText']
        }
    ]
}

server.run(port=8888, host='0.0.0.0',debug=True)