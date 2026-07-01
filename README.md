# Neural Translator Pro - 现代化多语言翻译系统

基于M2M-100模型的智能多语言翻译系统，支持100+种语言互译。

## 🌟 特性

- **现代化架构**：模块化设计，易于维护和扩展
- **多界面支持**：GUI界面、API服务、命令行
- **高性能翻译**：基于M2M-100模型，支持异步批量翻译
- **智能命名转换**：自动将翻译结果转换为驼峰命名
- **100+语言支持**：支持多种语言互译
- **本地部署**：数据安全，无需联网

## 📁 项目结构

```
translator_pro/
├── core/                    # 核心翻译引擎
│   ├── __init__.py
│   ├── translator.py        # 翻译器类
│   └── language_support.py  # 语言支持工具
├── gui/                     # 图形界面模块
│   ├── __init__.py
│   ├── main_window.py       # 主窗口
│   └── styles.py            # 现代化样式
├── api/                     # API服务模块
│   ├── __init__.py
│   └── server.py            # API服务器
├── config/                  # 配置模块
│   ├── __init__.py
│   └── settings.py          # 应用配置
├── utils/                   # 工具模块
│   ├── __init__.py
│   ├── logger.py            # 日志配置
│   └── helpers.py           # 辅助函数
├── main.py                  # 主启动脚本
├── run_gui.py               # GUI启动脚本
├── run_api.py               # API启动脚本
└── requirements.txt         # 依赖列表
```
## 模型下载
在开始前先去下载好模型，放到同目录下的models文件夹中
通过网盘分享的文件：models.zip
链接: https://pan.baidu.com/s/1eEnSZx5xP4JdL8bX-yf9Fw 提取码: z4wj 
--来自百度网盘超级会员v6的分享

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动应用

#### 启动GUI界面
```bash
python main.py --gui
# 或
python run_gui.py
```

#### 启动API服务器
```bash
python main.py --api --port 5000
# 或
python run_api.py --host 0.0.0.0 --port 5000
```

#### 同时启动GUI和API
```bash
python main.py --gui --api --port 5000
```

### 3. 使用API

#### 翻译文本
```bash
curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "你好世界",
    "src_lang": "zh",
    "tgt_lang": "en",
    "to_camel": true
  }'
```

#### 获取支持的语言
```bash
curl http://localhost:5000/languages
```

#### 健康检查
```bash
curl http://localhost:5000/health
```

## 📝 API文档

### POST /translate
翻译文本

**请求参数：**
```json
{
  "text": "要翻译的文本",
  "src_lang": "zh",      // 源语言代码
  "tgt_lang": "en",      // 目标语言代码
  "to_camel": false      // 是否转换为驼峰命名
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "original": "你好世界",
    "translated": "Hello World",
    "src_lang": "zh",
    "src_lang_name": "中文",
    "tgt_lang": "en",
    "tgt_lang_name": "英语",
    "camel_case": "helloWorld"  // 仅当to_camel=true且tgt_lang='en'时返回
  }
}
```

### POST /translate/batch
批量翻译

**请求参数：**
```json
{
  "texts": ["文本1", "文本2"],
  "src_lang": "zh",
  "tgt_lang": "en"
}
```

### GET /languages
获取支持的语言列表

**参数：**
- `chinese`: 是否使用中文名称（默认：true）

### GET /health
健康检查

### GET /model/info
获取模型信息

## ⚙️ 配置

配置文件位于 `config/settings.py`，支持以下配置：

### 模型配置
- `name`: 模型名称或路径
- `device`: 运行设备（cpu/cuda）
- `dtype`: 数据类型
- `max_length`: 最大输入长度
- `max_length_generate`: 最大生成长度
- `num_beams`: beam search数量

### 服务器配置
- `host`: 主机地址
- `port`: 端口号
- `debug`: 调试模式
- `allowed_ips`: 允许的IP列表

### GUI配置
- `window_title`: 窗口标题
- `window_width`: 窗口宽度
- `window_height`: 窗口高度
- `theme`: 主题

## 🔧 开发

### 代码规范
- 使用Python类型注解
- 遵循PEP8编码规范
- 使用中文注释

### 测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_translator.py
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 联系方式

如有问题，请通过GitHub Issues或者QQ邮箱3499643900@qq.com联系我们。
