/*
    real time subtitle translate for PotPlayer using aws API
*/

// string GetTitle()                                                         -> get title for UI
// string GetVersion                                                        -> get version for manage
// string GetDesc()                                                            -> get detail information
// string GetLoginTitle()                                                    -> get title for login dialog
// string GetLoginDesc()                                                    -> get desc for login dialog
// string ServerLogin(string User, string Pass)                                -> login
// string ServerLogout()                                                    -> logout
// array<string> GetDstLangs()                                                 -> get target language
// string Translate(string Text, string &in SrcLang, string &in DstLang)     -> do translate !!


string userAgent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36";//这个是可选配置，一般不用修改！

/**
* 获取当前插件的版本号
*/
string GetVersion(){
    return "1";
}

/**
* 获取当前插件的标题
*/
string GetTitle(){
    return "{$CP950=aws 翻譯$}{$CP0=aws translate$}";
}


/**
* 获取当前插件的表述信息
*/
string GetDesc(){
    return "https://aws.amazon.com/cn/transcribe/";
}

/**
* 获取登录的标题
*/
string GetLoginTitle(){
    return "aws翻译插件";
}

/**
* 获取登录的描述信息
*/
string GetLoginDesc(){
    return "请输入你的ak/sk,注意最小权限原则";
}


/**
* 获取登录时，用户输入框的标签名称
*/
string GetUserText(){
    return "ak:";
}

/**
* 获取登录时，密码输入框的标签名称
*/
string GetPasswordText(){
    return "sk:";
}


/**
* 获取支持的语言列表 - 源语言
*/
array<string> GetSrcLangs(){
    array<string> ret = GetLangTable();
    
    ret.insertAt(0, ""); // empty is auto
    return ret;
}

/**
* 获取支持的语言列表 - 目标语言
*/
array<string> GetDstLangs(){
    return GetLangTable();
}

/**
* 登录账号入口
*
// *  这里不做校验了，只要有输入就判定为成功。具体测试由用户的翻译测试按钮去测试
// * @param appIdStr appid 字符串
// * @param toKenStr 秘钥字符串
*/
// string ServerLogin(string appIdStr, string toKenStr){
//     //空字符串校验
//     if(appIdStr.empty() || toKenStr.empty()) return "fail";

//     //记录到全局变量中
//     appId = appIdStr;
//     toKen = toKenStr;
//     return "200 ok";
// }


/**
* 翻译的入口
* @param text 待翻译的原文
* @param srcLang 当前语言
* @param dstLang 目标语言
*/
string Translate(string text, string &in srcLang, string &in dstLang){
    string ret = "";
    if(!text.empty()){//确实有内容需要翻译才有必要继续
        //开发文档。需要App id 等信息
        HostOpenConsole();    // for debug
        
        //语言选择
        srcLang = GetLang(srcLang);
        dstLang = GetLang(dstLang);

        //对原文进行 url 编码
        string msg = HostUrlEncode(text);
        //HostPrintUTF8(q);
        //构建请求的 url 地址
        string url = "http://192.168.31.182:8888/translate?msg="+msg;

        //请求翻译
        string html = HostUrlGetString(url, userAgent);
        //HostPrintUTF8("Hello World!");

        //解析翻译结果
        ret = JsonParse(html);
        HostPrintUTF8(ret);

        if(ret.length() > 0){//如果有翻译结果
            srcLang = "UTF8";
            dstLang = "UTF8";
        }
    }
    return ret;
}

/**
* 获取语言
*/
string GetLang(string &in lang){
    string result = lang;

    if(result.empty()){//空字符串
        result = "auto";
    } else if(result == "zh-CN"){//简体中文
        result = "zh";
    } else if(result == "zh-TW"){//繁体中文
        result = "cht";
    } else if(result == "ja"){//日语
        result = "jp";
    } else if(result == "ro"){//罗马尼亚语
        result = "rom";
    }

    return result;
}


/**
* 支持的语言列表
*/
array<string> langTable = {
    "zh-CN",//->zh
    "zh-TW",//->cht
    "en",
    "ja",//->jp
    "kor",
    "fra",
    "spa",
    "th",
    "ara",
    "ru",
    "pt",
    "de",
    "it",
    "el",
    "nl",
    "pl",
    "bul",
    "est",
    "dan",
    "fin",
    "cs",
    "ro",//->rom
    "slo",
    "swe",
    "hu",
    "vie",
    "yue",//粤语
    "wyw",//文言文
};

/**
* 获取支持语言
*/
array<string>  GetLangTable(){
    return langTable;
}

/**
* 解析Json数据
* @param json 服务器返回的Json字符串
*/
string JsonParse(string json){
    string ret = "";//返回值
    JsonReader reader;
    JsonValue root;
    
    if (reader.parse(json, root)){//如果成功解析了json内容
        if(root.isObject()){//要求是对象模式
            array<string> keys = root.getKeys();//获取json root对象中所有的key
            //查找是否存在错误
            if(hasErrorInResult(keys)){//如果发生了错误
                JsonValue errorCode = root["error_code"];//错误编号
                JsonValue errorMsg = root["error_msg"];//错误信息描述
                ret = "error: " + errorCode.asString() + ", error_msg=" + errorMsg.asString();
            }else{//如果没发生错误
                JsonValue transResult = root["trans_result"];//取得翻译结果
                if(transResult.isArray()){//如果有翻译结果-必须是数组形式
                    for(int i = 0; i < transResult.size(); i++){
                        JsonValue item = transResult[i];//取得翻译结果
                        JsonValue dst = item["dst"];//获取翻译结果的目标
                        if(i > 0){//如果需要处理多行的情况
                            ret += "\n";//第二行开始的开头位置，加上换行符
                        }
                        ret += dst.asString();//拼接翻译结果，可能存在多行
                    }
                }
            }
        }
    } 
    return ret;
}

/**
* 检查翻译结果返回值中是否存在错误
* @param keys json root 层的 key 列表
*/
bool hasErrorInResult(array<string> keys){
    bool result = false;
    for(uint i = 0; i < keys.size(); i++){
        if("error_code" == keys[i]){
            result = true;
            break;
        }
    }
    return result;
}