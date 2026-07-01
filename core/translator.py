"""
核心翻译引擎 - 基于M2M-100模型
"""
import torch
import logging
import time
import asyncio
import threading
from typing import List, Dict, Optional, Union
from functools import lru_cache
from pathlib import Path

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Translator:
    """现代化的多语言翻译器，使用 M2M-100 模型"""
    
    def __init__(self, model_name: str = './models', debug: bool = False):
        """
        初始化翻译器
        
        Args:
            model_name: 模型名称或路径
            debug: 是否启用调试模式
        """
        self.model_name = model_name
        self.debug = debug
        self.model = None
        self.tokenizer = None
        self._lock = threading.Lock()
        self.load_time = 0
        self._loaded = False
        
    def load_model(self):
        """从本地加载模型（线程安全）"""
        with self._lock:
            if self._loaded:
                return
            
            try:
                from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer
                
                if self.debug:
                    logger.info(f"从本地加载模型: {self.model_name}")
                
                start_time = time.time()
                
                # 检查模型路径
                model_path = Path(self.model_name)
                if not model_path.exists():
                    raise FileNotFoundError(f"模型路径 {self.model_name} 不存在，请检查目录！")
                
                # 加载tokenizer和模型
                self.tokenizer = M2M100Tokenizer.from_pretrained(
                    self.model_name,
                    local_files_only=True
                )
                
                self.model = M2M100ForConditionalGeneration.from_pretrained(
                    self.model_name,
                    dtype=torch.float32,
                    low_cpu_mem_usage=True,
                    local_files_only=True
                )
                
                self.model.eval()
                self.load_time = time.time() - start_time
                self._loaded = True
                
                if self.debug:
                    logger.info(f"模型加载成功，耗时: {self.load_time:.2f}秒")
                    
            except Exception as e:
                logger.error(f"加载模型失败: {e}")
                raise
    
    @lru_cache(maxsize=1000)
    def _translate_single(self, text: str, src_lang: str = 'zh', tgt_lang: str = 'en') -> str:
        """
        同步单条翻译，支持指定源和目标语言
        
        Args:
            text: 输入文本
            src_lang: 源语言代码
            tgt_lang: 目标语言代码
            
        Returns:
            翻译后的文本
        """
        if not text or not text.strip():
            return text
        
        if not self.model or not self.tokenizer:
            if self.debug:
                logger.warning("模型未初始化")
            return text
        
        try:
            self.tokenizer.src_lang = src_lang
            inputs = self.tokenizer(
                text, 
                return_tensors="pt", 
                padding=True, 
                truncation=True, 
                max_length=128
            )
            
            with torch.no_grad():
                translated = self.model.generate(
                    **inputs,
                    max_length=150,
                    num_beams=2,
                    early_stopping=True,
                    do_sample=False,
                    forced_bos_token_id=self.tokenizer.get_lang_id(tgt_lang)
                )
            
            result = self.tokenizer.decode(translated[0], skip_special_tokens=True)
            return result.strip() if result else ""
            
        except Exception as e:
            if self.debug:
                logger.error(f"翻译失败: {e}")
            return ""
    
    async def _translate_async(self, text: str, src_lang: str = 'zh', tgt_lang: str = 'en') -> str:
        """
        异步单条翻译
        
        Args:
            text: 输入文本
            src_lang: 源语言代码
            tgt_lang: 目标语言代码
            
        Returns:
            翻译后的文本
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._translate_single, text, src_lang, tgt_lang)
    
    async def _translate_batch_async(self, texts: List[str], src_lang: str = 'zh', tgt_lang: str = 'en') -> List[str]:
        """
        异步批量翻译
        
        Args:
            texts: 输入文本列表
            src_lang: 源语言代码
            tgt_lang: 目标语言代码
            
        Returns:
            翻译后的文本列表
        """
        if not texts:
            return []
        
        tasks = [self._translate_async(text, src_lang, tgt_lang) for text in texts]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [str(result) if not isinstance(result, Exception) else "" for result in results]
    
    def translate_batch(self, texts: List[str], src_lang: str = 'zh', tgt_lang: str = 'en') -> List[str]:
        """
        同步批量翻译
        
        Args:
            texts: 输入文本列表
            src_lang: 源语言代码
            tgt_lang: 目标语言代码
            
        Returns:
            翻译后的文本列表
        """
        if not texts:
            return []
        
        if not self.model or not self.tokenizer:
            if self.debug:
                logger.warning("模型未初始化")
            return texts
        
        try:
            valid_texts = [text for text in texts if text and text.strip()]
            if not valid_texts:
                return [""] * len(texts)
            
            self.tokenizer.src_lang = src_lang
            inputs = self.tokenizer(
                valid_texts, 
                return_tensors="pt", 
                padding=True, 
                truncation=True, 
                max_length=128
            )
            
            with torch.no_grad():
                translated = self.model.generate(
                    **inputs,
                    max_length=150,
                    num_beams=2,
                    early_stopping=True,
                    do_sample=False,
                    forced_bos_token_id=self.tokenizer.get_lang_id(tgt_lang)
                )
            
            results = self.tokenizer.batch_decode(translated, skip_special_tokens=True)
            results = [r.strip() for r in results]
            
            final_results = []
            text_iter = iter(results)
            for text in texts:
                if text and text.strip():
                    final_results.append(next(text_iter))
                else:
                    final_results.append("")
            
            return final_results
            
        except Exception as e:
            if self.debug:
                logger.error(f"批量翻译失败: {e}")
            return texts
    
    def translate(self, text: Union[str, List[str]], src_lang: str = 'zh', tgt_lang: str = 'en') -> Union[str, List[str]]:
        """
        统一翻译接口
        
        Args:
            text: 输入文本（单条或批量）
            src_lang: 源语言代码
            tgt_lang: 目标语言代码
            
        Returns:
            翻译后的文本
        """
        if isinstance(text, str):
            return self._translate_single(text, src_lang, tgt_lang)
        else:
            return self.translate_batch(text, src_lang, tgt_lang)
    
    def get_model_info(self) -> Dict:
        """获取模型信息"""
        return {
            'model_name': self.model_name,
            'loaded': self._loaded,
            'load_time': f"{self.load_time:.2f}s" if self._loaded else "未加载",
            'device': 'CPU',
            'dtype': 'float32'
        }
