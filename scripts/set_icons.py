import os
import platform
from PyQt5.QtGui import QIcon
import sys

def set_application_icon(app):
    """根据平台自动设置应用图标"""
    system = platform.system()
    
    icon_path = None
    if system == "Darwin":  # macOS
        icon_path = "assets/icons/app_icon.icns"
    elif system == "Windows":  # Windows
        icon_path = "assets/icons/app_icon.ico"
    else:  # Linux及其他
        icon_path = "assets/icons/app_icon.png"
    
    if icon_path and os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        print(f"应用图标已设置为: {icon_path}")
    else:
        print(f"警告: 图标文件未找到: {icon_path}")

if __name__ == "__main__":
    # 测试图标设置
    from PyQt5.QtWidgets import QApplication, QMainWindow
    
    app = QApplication(sys.argv)
    set_application_icon(app)
    
    window = QMainWindow()
    window.setWindowTitle("SkipAudioMaker - 图标测试")
    window.show()
    
    sys.exit(app.exec_())