"""
API服务器模块 - 提供RESTful API接口
"""
import os
import sys
import logging
from typing import Dict, List, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import Translator, LanguageSupport

logger = logging.getLogger(__name__)


class TranslationAPI:
    """翻译API类"""
    
    def __init__(self, translator: Translator):
        """
        初始化API
        
        Args:
            translator: 翻译器实例
        """
        self.translator = translator
        self.app = Flask(__name__)
        CORS(self.app)  # 启用跨域支持
        
        # 注册路由
        self._register_routes()
    
    def _register_routes(self):
        """注册API路由"""
        
        @self.app.route('/', methods=['GET'])
        def index():
            """首页"""
            return jsonify({
                'name': 'Neural Translator Pro API',
                'version': '2.0.0',
                'description': '基于M2M-100模型的多语言翻译API',
                'endpoints': {
                    '/translate': 'POST - 翻译文本',
                    '/languages': 'GET - 获取支持的语言列表',
                    '/health': 'GET - 健康检查',
                    '/model/info': 'GET - 获取模型信息'
                }
            })
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """健康检查"""
            return jsonify({
                'status': 'healthy',
                'translator_loaded': self.translator._loaded
            })
        
        @self.app.route('/languages', methods=['GET'])
        def get_languages():
            """获取支持的语言列表"""
            use_chinese = request.args.get('chinese', 'true').lower() == 'true'
            languages = LanguageSupport.get_all_languages(use_chinese=use_chinese)
            return jsonify({
                'languages': [{'code': code, 'name': name} for code, name in languages],
                'total': len(languages)
            })
        
        @self.app.route('/model/info', methods=['GET'])
        def get_model_info():
            """获取模型信息"""
            return jsonify(self.translator.get_model_info())
        
        @self.app.route('/translate', methods=['POST'])
        def translate():
            """翻译文本"""
            try:
                data = request.get_json()
                
                if not data:
                    return jsonify({'error': '请求体不能为空'}), 400
                
                # 获取参数
                text = data.get('text', '')
                src_lang = data.get('src_lang', 'zh')
                tgt_lang = data.get('tgt_lang', 'en')
                to_camel = data.get('to_camel', False)
                
                # 验证参数
                if not text:
                    return jsonify({'error': '文本不能为空'}), 400
                
                if not LanguageSupport.is_valid_language(src_lang):
                    return jsonify({'error': f'无效的源语言代码: {src_lang}'}), 400
                
                if not LanguageSupport.is_valid_language(tgt_lang):
                    return jsonify({'error': f'无效的目标语言代码: {tgt_lang}'}), 400
                
                # 执行翻译
                translated = self.translator.translate(text, src_lang, tgt_lang)
                
                # 构建响应
                response = {
                    'success': True,
                    'data': {
                        'original': text,
                        'translated': translated,
                        'src_lang': src_lang,
                        'src_lang_name': LanguageSupport.get_language_name(src_lang, use_chinese=True),
                        'tgt_lang': tgt_lang,
                        'tgt_lang_name': LanguageSupport.get_language_name(tgt_lang, use_chinese=True)
                    }
                }
                
                # 如果需要驼峰命名
                if to_camel and tgt_lang == 'en':
                    camel_case = LanguageSupport.process_translation_to_camel(translated, text, src_lang)
                    response['data']['camel_case'] = camel_case
                
                return jsonify(response)
                
            except Exception as e:
                logger.error(f"翻译失败: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/translate/batch', methods=['POST'])
        def translate_batch():
            """批量翻译"""
            try:
                data = request.get_json()
                
                if not data:
                    return jsonify({'error': '请求体不能为空'}), 400
                
                # 获取参数
                texts = data.get('texts', [])
                src_lang = data.get('src_lang', 'zh')
                tgt_lang = data.get('tgt_lang', 'en')
                
                # 验证参数
                if not texts:
                    return jsonify({'error': '文本列表不能为空'}), 400
                
                if not isinstance(texts, list):
                    return jsonify({'error': 'texts必须是数组'}), 400
                
                if not LanguageSupport.is_valid_language(src_lang):
                    return jsonify({'error': f'无效的源语言代码: {src_lang}'}), 400
                
                if not LanguageSupport.is_valid_language(tgt_lang):
                    return jsonify({'error': f'无效的目标语言代码: {tgt_lang}'}), 400
                
                # 执行批量翻译
                translated_list = self.translator.translate(texts, src_lang, tgt_lang)
                
                # 构建响应
                results = []
                for original, translated in zip(texts, translated_list):
                    results.append({
                        'original': original,
                        'translated': translated
                    })
                
                response = {
                    'success': True,
                    'data': {
                        'results': results,
                        'src_lang': src_lang,
                        'src_lang_name': LanguageSupport.get_language_name(src_lang, use_chinese=True),
                        'tgt_lang': tgt_lang,
                        'tgt_lang_name': LanguageSupport.get_language_name(tgt_lang, use_chinese=True),
                        'total': len(results)
                    }
                }
                
                return jsonify(response)
                
            except Exception as e:
                logger.error(f"批量翻译失败: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500


def create_api_server(host: str = '0.0.0.0', port: int = 5000, debug: bool = False) -> Flask:
    """
    创建API服务器
    
    Args:
        host: 主机地址
        port: 端口号
        debug: 是否启用调试模式
        
    Returns:
        Flask应用实例
    """
    # 初始化翻译器
    # 从当前文件向上一级到translator_pro目录，然后找models文件夹
    model_path = os.path.join(os.path.dirname(__file__), '..', 'models')
    if not os.path.exists(model_path):
        # 如果不存在，尝试当前目录下的models
        model_path = './models'
    
    translator = Translator(model_name=model_path, debug=debug)
    translator.load_model()
    
    # 创建API
    api = TranslationAPI(translator)
    
    return api.app


if __name__ == '__main__':
    # 直接运行API服务器
    app = create_api_server(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
