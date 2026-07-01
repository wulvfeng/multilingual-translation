"""
Neural Translator Pro - 主启动脚本
支持多种启动模式：GUI、API、同时启动
"""
import sys
import os
import argparse
import threading

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_gui():
    """运行GUI界面"""
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import Qt
    from gui import TranslatorMainWindow
    
    # 启用高DPI支持
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Neural Translator Pro")
    app.setStyle("Fusion")
    
    window = TranslatorMainWindow()
    window.show()
    window.activateWindow()  # 确保窗口激活
    window.raise_()  # 将窗口提升到最前面
    
    return app


def run_api(host='0.0.0.0', port=5000, debug=False):
    """运行API服务器"""
    from api import create_api_server
    
    app = create_api_server(host=host, port=port, debug=debug)
    app.run(host=host, port=port, debug=debug, use_reloader=False)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='Neural Translator Pro - 现代化多语言翻译系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 启动GUI界面
  python main.py --gui
  
  # 启动API服务器
  python main.py --api --port 5000
  
  # 同时启动GUI和API
  python main.py --gui --api --port 5000
  
  # 仅启动API服务器（后台线程）
  python main.py --api --background --port 5000
        """
    )
    
    parser.add_argument('--gui', action='store_true', help='启动图形界面')
    parser.add_argument('--api', action='store_true', help='启动API服务器')
    parser.add_argument('--host', default='0.0.0.0', help='API服务器主机地址 (默认: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='API服务器端口号 (默认: 5000)')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    parser.add_argument('--background', action='store_true', help='在后台线程中启动API服务器')
    
    args = parser.parse_args()
    
    # 如果没有指定任何参数，默认启动GUI
    if not args.gui and not args.api:
        args.gui = True
    
    print("\n" + "="*60)
    print("🌍 Neural Translator Pro - 现代化多语言翻译系统")
    print("📦 版本: 2.0.0")
    print("="*60 + "\n")
    
    # 启动API服务器（如果需要）
    if args.api:
        if args.background:
            # 在后台线程中启动API
            api_thread = threading.Thread(
                target=run_api,
                args=(args.host, args.port, args.debug),
                daemon=True
            )
            api_thread.start()
            print(f"🌐 API服务器已在后台启动: http://{args.host}:{args.port}")
        else:
            # 如果只启动API，直接运行
            if not args.gui:
                print(f"🌐 启动API服务器: http://{args.host}:{args.port}")
                run_api(args.host, args.port, args.debug)
                return
            else:
                # GUI和API同时启动，API在后台
                api_thread = threading.Thread(
                    target=run_api,
                    args=(args.host, args.port, args.debug),
                    daemon=True
                )
                api_thread.start()
                print(f"🌐 API服务器已在后台启动: http://{args.host}:{args.port}")
    
    # 启动GUI（如果需要）
    if args.gui:
        print("🎨 启动图形界面...")
        app = run_gui()
        
        print("\n" + "="*60)
        print("✅ 系统启动完成！")
        if args.api:
            print(f"🌐 API服务器: http://{args.host}:{args.port}")
        print("🎨 图形界面已打开")
        print("💡 提示：请确保模型文件已放置在正确位置")
        print("="*60 + "\n")
        
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
