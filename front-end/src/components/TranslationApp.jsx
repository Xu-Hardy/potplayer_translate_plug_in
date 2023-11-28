import React, { useState } from 'react';
import axios from 'axios';
import '../styles/TranslationApp.css';
import config from '../../config/config';

function TranslationApp() {
    const [input, setInput] = useState('');
    const [translation, setTranslation] = useState('');
    const [isEngToChn, setIsEngToChn] = useState(true);

    const handleInputChange = async (e) => {
        const textarea = e.target;
        const value = textarea.value;
        setInput(value);

        textarea.style.height = "auto";
        textarea.style.height = (textarea.scrollHeight) + "px";

        const translatedText = await translateText(value);
        setTranslation(translatedText);
    };

    const toggleTranslationDirection = () => {
        setIsEngToChn(!isEngToChn);
        setInput('');
        setTranslation('');
    }

    const translateText = async (text) => {
        try {
            let src, dst;
            // let src, dst;
            // const direction = isEngToChn ? "eng-to-chn" : "chn-to-eng";
            if (isEngToChn){
                src = 'en';
                dst = 'zh'
            }else {
                src = 'zh';
                dst = 'en'
            }
            const response = await axios.post(config.apiUrl, {
                msg: text,
                src: src,
                dst:dst
            });

            if (response.data.trans_result && response.data.trans_result.length > 0) {
                return response.data.trans_result[0].dst;
            } else {
                console.error("Unexpected response structure:", response.data);
                return text;
            }

        } catch (error) {
            console.error("Error during translation:", error);
            return text;
        }
    };

    return (
        <div className="translation-container">
            <h1 className="translation-title">实时翻译</h1>
            <button className="toggle-button" onClick={toggleTranslationDirection}>
                {isEngToChn ? "English -> 中文" : "中文 -> English"}
            </button>
            <div className="translation-app">
                <div className="input-container">
                    <h2>{isEngToChn ? "英文输入" : "中文输入"}</h2>
                    <textarea
                        placeholder={isEngToChn ? "输入英文..." : "输入中文..."}
                        value={input}
                        onChange={handleInputChange}
                    />
                </div>
                <div className="output-container">
                    <h2>{isEngToChn ? "中文翻译" : "英文翻译"}</h2>
                    <div className="translation-output">{translation}</div>
                </div>
            </div>
        </div>
    );
}

export default TranslationApp;
