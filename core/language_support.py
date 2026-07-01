"""
语言支持模块 - 语言映射和文本处理
"""
import re
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class LanguageSupport:
    """语言支持工具类"""
    
    # 支持的语言映射（中文名称）
    LANGUAGE_MAP_CN = {
        'af': '南非荷兰语', 'am': '阿姆哈拉语', 'ar': '阿拉伯语', 'as': '阿萨姆语', 'ast': '阿斯图里亚斯语',
        'az': '阿塞拜疆语', 'ba': '巴什基尔语', 'be': '白俄罗斯语', 'bg': '保加利亚语', 'bn': '孟加拉语',
        'br': '布列塔尼语', 'bs': '波斯尼亚语', 'ca': '加泰罗尼亚语', 'ceb': '宿务语', 'cs': '捷克语',
        'cy': '威尔士语', 'da': '丹麦语', 'de': '德语', 'el': '希腊语', 'en': '英语',
        'et': '爱沙尼亚语', 'fa': '波斯语', 'ff': '富拉语', 'fi': '芬兰语', 'fr': '法语',
        'fy': '西弗里西亚语', 'ga': '爱尔兰语', 'gd': '苏格兰盖尔语', 'gl': '加利西亚语', 'gu': '古吉拉特语',
        'ha': '豪萨语', 'he': '希伯来语', 'hi': '印地语', 'hr': '克罗地亚语', 'ht': '海地克里奥尔语',
        'hu': '匈牙利语', 'hy': '亚美尼亚语', 'id': '印尼语', 'ig': '伊博语', 'ilo': '伊洛卡诺语',
        'is': '冰岛语', 'it': '意大利语', 'ja': '日语', 'jv': '爪哇语', 'ka': '格鲁吉亚语',
        'kk': '哈萨克语', 'gom': '孔卡尼语', 'ko': '韩语', 'ku': '库尔德语', 'ky': '吉尔吉斯语',
        'la': '拉丁语', 'lb': '卢森堡语', 'ln': '林加拉语', 'lt': '立陶宛语', 'lv': '拉脱维亚语',
        'mg': '马达加斯加语', 'mk': '马其顿语', 'ml': '马拉雅拉姆语', 'mn': '蒙古语', 'mr': '马拉地语',
        'ms': '马来语', 'my': '缅甸语', 'ne': '尼泊尔语', 'nl': '荷兰语', 'no': '挪威语',
        'ns': '北索托语', 'oc': '奥克语', 'or': '奥里亚语', 'pa': '旁遮普语', 'pl': '波兰语',
        'ps': '普什图语', 'pt': '葡萄牙语', 'ro': '罗马尼亚语', 'ru': '俄语', 'rw': '卢旺达语',
        'sd': '信德语', 'si': '僧伽罗语', 'sk': '斯洛伐克语', 'sl': '斯洛文尼亚语', 'so': '索马里语',
        'sq': '阿尔巴尼亚语', 'sr': '塞尔维亚语', 'su': '巽他语', 'sv': '瑞典语', 'sw': '斯瓦希里语',
        'ta': '泰米尔语', 'te': '泰卢固语', 'tg': '塔吉克语', 'th': '泰语', 'tk': '土库曼语',
        'tr': '土耳其语', 'tt': '鞑靼语', 'ug': '维吾尔语', 'uk': '乌克兰语', 'ur': '乌尔都语',
        'uz': '乌兹别克语', 'vi': '越南语', 'wo': '沃洛夫语', 'xh': '科萨语', 'yi': '意第绪语',
        'yo': '约鲁巴语', 'zh': '中文', 'zu': '祖鲁语'
    }
    
    # 支持的语言映射（英文名称）
    LANGUAGE_MAP_EN = {
        'af': 'Afrikaans', 'am': 'Amharic', 'ar': 'Arabic', 'as': 'Assamese', 'ast': 'Asturian',
        'az': 'Azerbaijani', 'ba': 'Bashkir', 'be': 'Belarusian', 'bg': 'Bulgarian', 'bn': 'Bengali',
        'br': 'Breton', 'bs': 'Bosnian', 'ca': 'Catalan', 'ceb': 'Cebuano', 'cs': 'Czech',
        'cy': 'Welsh', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English',
        'et': 'Estonian', 'fa': 'Persian', 'ff': 'Fulah', 'fi': 'Finnish', 'fr': 'French',
        'fy': 'Western Frisian', 'ga': 'Irish', 'gd': 'Gaelic', 'gl': 'Galician', 'gu': 'Gujarati',
        'ha': 'Hausa', 'he': 'Hebrew', 'hi': 'Hindi', 'hr': 'Croatian', 'ht': 'Haitian',
        'hu': 'Hungarian', 'hy': 'Armenian', 'id': 'Indonesian', 'ig': 'Igbo', 'ilo': 'Iloko',
        'is': 'Icelandic', 'it': 'Italian', 'ja': 'Japanese', 'jv': 'Javanese', 'ka': 'Georgian',
        'kk': 'Kazakh', 'gom': 'Konkani', 'ko': 'Korean', 'ku': 'Kurdish', 'ky': 'Kyrgyz',
        'la': 'Latin', 'lb': 'Luxembourgish', 'ln': 'Lingala', 'lt': 'Lithuanian', 'lv': 'Latvian',
        'mg': 'Malagasy', 'mk': 'Macedonian', 'ml': 'Malayalam', 'mn': 'Mongolian', 'mr': 'Marathi',
        'ms': 'Malay', 'my': 'Burmese', 'ne': 'Nepali', 'nl': 'Dutch', 'no': 'Norwegian',
        'ns': 'Northern Sotho', 'oc': 'Occitan', 'or': 'Oriya', 'pa': 'Punjabi', 'pl': 'Polish',
        'ps': 'Pashto', 'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian', 'rw': 'Kinyarwanda',
        'sd': 'Sindhi', 'si': 'Sinhala', 'sk': 'Slovak', 'sl': 'Slovenian', 'so': 'Somali',
        'sq': 'Albanian', 'sr': 'Serbian', 'su': 'Sundanese', 'sv': 'Swedish', 'sw': 'Swahili',
        'ta': 'Tamil', 'te': 'Telugu', 'tg': 'Tajik', 'th': 'Thai', 'tk': 'Turkmen',
        'tr': 'Turkish', 'tt': 'Tatar', 'ug': 'Uighur', 'uk': 'Ukrainian', 'ur': 'Urdu',
        'uz': 'Uzbek', 'vi': 'Vietnamese', 'wo': 'Wolof', 'xh': 'Xhosa', 'yi': 'Yiddish',
        'yo': 'Yoruba', 'zh': 'Chinese', 'zu': 'Zulu'
    }
    
    @classmethod
    def get_language_name(cls, code: str, use_chinese: bool = True) -> str:
        """
        获取语言名称
        
        Args:
            code: 语言代码
            use_chinese: 是否使用中文名称
            
        Returns:
            语言名称
        """
        if use_chinese:
            return cls.LANGUAGE_MAP_CN.get(code, code)
        return cls.LANGUAGE_MAP_EN.get(code, code)
    
    @classmethod
    def get_all_languages(cls, use_chinese: bool = True) -> List[tuple]:
        """
        获取所有支持的语言
        
        Args:
            use_chinese: 是否使用中文名称
            
        Returns:
            语言代码和名称的列表
        """
        lang_map = cls.LANGUAGE_MAP_CN if use_chinese else cls.LANGUAGE_MAP_EN
        return sorted(lang_map.items(), key=lambda x: x[1])
    
    @classmethod
    def is_valid_language(cls, code: str) -> bool:
        """
        检查语言代码是否有效
        
        Args:
            code: 语言代码
            
        Returns:
            是否有效
        """
        return code in cls.LANGUAGE_MAP_CN
    
    @classmethod
    def to_pinyin_camel_case(cls, text: str, src_lang: str = 'zh') -> str:
        """
        将文本转换为驼峰命名（中文使用拼音）
        
        Args:
            text: 输入文本
            src_lang: 源语言代码
            
        Returns:
            驼峰命名文本
        """
        if not text or not text.strip():
            return text
        
        try:
            if src_lang == 'zh':
                import pypinyin
                pinyin_list = pypinyin.lazy_pinyin(text, style=pypinyin.Style.NORMAL, errors='ignore')
                pinyin_list = [pinyin for pinyin in pinyin_list if pinyin and pinyin.strip()]
                
                if not pinyin_list:
                    return text
                
                camel_case = pinyin_list[0].lower()
                for pinyin in pinyin_list[1:]:
                    if pinyin:
                        camel_case += pinyin[0].upper() + pinyin[1:].lower()
                
                camel_case = re.sub(r'[^a-zA-Z0-9]', '', camel_case)
                
                if not camel_case:
                    simplified = re.sub(r'[^a-zA-Z0-9]', '', text)
                    return simplified.lower() if simplified else "defaultVar"
                
                return camel_case
            
            # 非中文语言直接清理
            simplified = re.sub(r'[^a-zA-Z0-9]', '', text)
            return simplified.lower() if simplified else "defaultVar"
            
        except Exception as e:
            logger.error(f"转换失败: {e}")
            simplified = re.sub(r'[^a-zA-Z0-9]', '', text)
            return simplified.lower() if simplified else "defaultVar"
    
    @classmethod
    def process_translation_to_camel(cls, translated: str, original: str, src_lang: str = 'zh') -> str:
        """
        处理翻译结果，转换为驼峰命名
        
        Args:
            translated: 翻译后的文本
            original: 原始文本
            src_lang: 源语言代码
            
        Returns:
            驼峰命名文本
        """
        if not translated:
            return cls.to_pinyin_camel_case(original, src_lang)
        
        try:
            cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', translated)
            words = cleaned_text.split()
            
            if not words:
                return cls.to_pinyin_camel_case(original, src_lang)
            
            camel_case = words[0].lower()
            for word in words[1:]:
                if word:
                    camel_case += word[0].upper() + word[1:].lower()
            
            return camel_case
            
        except Exception as e:
            logger.error(f"处理翻译结果出错: {e}")
            return cls.to_pinyin_camel_case(original, src_lang)
