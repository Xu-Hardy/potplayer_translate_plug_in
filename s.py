from flask import Flask, request
import boto3

server=Flask(__name__)

ak,sk='',''
client = boto3.client('translate',region_name=ak, aws_access_key_id=sk)

@server.route('/translate',methods=['post','get'])
def get_time():
    # data = request.args
    # source_lanuage = data.get('src')
    # destination_lanuage = data.get('dst')
    # message = data.get('msg')
    # print(data)

    source_lanuage = 'en'
    destination_lanuage = 'zh'
    print(request.args)
    data = request.args
    message = data.get('q')
    print(message)
    response=client.translate_text(
    Text=message,
    SourceLanguageCode=source_lanuage,
    TargetLanguageCode=destination_lanuage,
    )

    # print(response['TranslatedText'])

    return {
        "from": f"",
        "to": f"{destination_lanuage}",
        "trans_result": [
        {
            "src": message,
            "dst": response['TranslatedText']
        }
    ]
}


server.run(port=8888, host='0.0.0.0',debug=True)