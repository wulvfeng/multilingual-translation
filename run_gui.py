"""
启动GUI界面
"""
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from gui import TranslatorMainWindow


def main():
    """主函数"""
    print("\n" + "="*60)
    print("🚀 Neural Translator Pro - 现代化多语言翻译系统")
    print("🎨 启动图形界面...")
    print("="*60 + "\n")
    
    # 高DPI缩放支持（必须在QApplication创建前设置）
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Neural Translator Pro")
    app.setOrganizationName("Translator Pro")
    
    # 设置应用程序样式
    app.setStyle("Fusion")
    
    # 创建并显示主窗口
    window = TranslatorMainWindow()
    window.show()
    
    print("✅ 界面启动成功！")
    print("💡 提示：请确保模型文件已放置在正确位置")
    print("="*60 + "\n")
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
