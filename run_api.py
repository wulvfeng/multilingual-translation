"""
启动API服务器
"""
import sys
import os
import argparse

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api import create_api_server


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='启动翻译API服务器')
    parser.add_argument('--host', default='0.0.0.0', help='主机地址 (默认: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='端口号 (默认: 5000)')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("🚀 Neural Translator Pro - API服务器")
    print(f"🌐 启动地址: http://{args.host}:{args.port}")
    print("="*60 + "\n")
    
    # 创建并启动API服务器
    app = create_api_server(host=args.host, port=args.port, debug=args.debug)
    
    print("✅ API服务器启动成功！")
    print("📖 API文档:")
    print("   GET  /           - 首页")
    print("   GET  /health     - 健康检查")
    print("   GET  /languages  - 获取支持的语言列表")
    print("   GET  /model/info - 获取模型信息")
    print("   POST /translate  - 翻译文本")
    print("   POST /translate/batch - 批量翻译")
    print("="*60 + "\n")
    
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
