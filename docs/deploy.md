# 部署

## 部署步骤

1. 把Extension目录下的SubtitleTranslate - aws.as放在potplayer对应目录中，对我来说，这个是C:\Program Files\DAUM\PotPlayer\Extension\Subtitle\Translate
2. 运行translate_api目录下的app.py
3. 然后把SubtitleTranslate - aws.as中的请求链接改成本地的路由
http://localhost:5000/translate?msg=dog
```bash
./deploy.sh
```
4. 如需使用容器部署, 目录下也提供了对应的dockerfile
```bash
docker build -t awstranslate .
docker run -p 5000:5000 awstranslate
```
## 工程结构

```text
.
├── Extension
│   └── SubtitleTranslate\ -\ aws.as
├── README.md
├── dockerfile
├── docs
│   ├── about.md
│   └── deploy.md
├── images
│   ├── img.png
│   ├── img_1.png
│   └── img_2.png
├── requirements.txt\ 
└── translate_api
    └── app.py
```
