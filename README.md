# potplayer_translate_plug_in

本文参考大佬的百度插件进行二次开发：https://github.com/fjqingyou/PotPlayer_Subtitle_Translate_Baidu

PotPlayer 字幕在线翻译插件- 基于aws transcribe翻译的potplayer实时字幕



## 安装说明

1. 安装potplayer，官网是https://potplayer.daum.net/
2. 下载项目脚本，git clone git@github.com:Xu-Hardy/potplayer_translate_plug_in.git
3. 安装Python和依赖，这里推荐[miniconda](https://docs.conda.io/projects/miniconda/en/latest/index.html)和[pip清华源](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/) 

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

4. 运行翻译后端,进入translate_api目录，然后执行：

```bash
pip install -r requirements.txt
```

然后把AWS 海外区的ak/sk写到.env中，格式参考temp.env

```
python translate.py
```

然后浏览器打开http://localhost:50000来查看服务是否正常运行

5. 安装播放器脚本，把Extension目录下的`1SubtitleTranslate - aws.as`和`SubtitleTranslate - aws.ico`放到`C:\Program Files\DAUM\PotPlayer\Extension\Subtitle\Translate`这个目录，如果你的默认路径不是这个，那么按照如图所示

![](https://raw.githubusercontent.com/Xu-Hardy/image-host/master/20231122141837.png)

这里打开文件夹可以看到你的potplayer插件目录，然后点击账户设置。

![](https://raw.githubusercontent.com/Xu-Hardy/image-host/master/20231122141908.png)

填写刚刚运行的python脚本的地址，http://yourip:50000/pt，apiley随意。

![](https://raw.githubusercontent.com/Xu-Hardy/image-host/master/20231122142415.png)

声明：本程序不提供任何aws的凭证，也不会采集任何凭证，源码均已开放

## 基于aws翻译的potplayer实时字幕

具体部署步骤可以见[部署文档](docs/deploy.md)

了解，我会为你提供一个中英对照的项目介绍说明。

---

**Using the PopLayer Plugin with AWS Translation API - Project Introduction**

**使用 PopLayer 插件与 AWS 翻译 API - 项目介绍**

This project integrates the dynamic functionalities of the PopLayer plugin with the robust AWS Translation API. By harnessing the capabilities of both, we aim to offer real-time translation features for applications and websites seamlessly.

此项目将 PopLayer 插件的动态功能与强大的 AWS 翻译 API 整合在一起。通过结合两者的功能，我们旨在为应用程序和网站无缝地提供实时翻译功能。

**Features | 功能**
1. Real-time translation: Translate content instantaneously without the need to refresh or reload.
   实时翻译：无需刷新或重新加载即可瞬间翻译内容。

2. Pop-up interface: Leveraging the PopLayer plugin, translations are shown in a user-friendly pop-up interface.
   弹出界面：利用 PopLayer 插件，翻译内容将在用户友好的弹出界面中显示。

3. Support for multiple languages: With AWS Translation API, we offer translation for a wide range of languages.
   支持多种语言：借助 AWS 翻译 API，我们提供多种语言的翻译。

**Applications | 应用场景**
Ideal for websites and applications with a diverse user base, aiming to provide multilingual support without compromising user experience.
适用于拥有多元用户群的网站和应用程序，目标是在不影响用户体验的情况下提供多语言支持。

**Future Prospects | 未来展望**
We aim to expand the range of supported languages and refine the integration for smoother user experiences.
我们计划扩展支持的语言范围，并优化集成以提供更流畅的用户体验。

---

希望这个中英对照的项目介绍可以满足您的需求！如果有其他需要，请告诉我。
## 语言支持

2022/11/22 支持英文翻译成中文
2023/10/30 支持输入api地址和apikey


最后：

欢迎大家提pull request。

https://github.com/mengze-han/potplayer_translate_plug_in
