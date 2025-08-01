import sys
import os
import logging
from PyQt5.QtWidgets import QApplication, QSplashScreen, QMessageBox
from PyQt5.QtGui import QPixmap, QFont
from gui.main_window import MainWindow
from utils.brand_colors import BrandColors
from utils.brand_fonts import BrandFonts

# 设置 FFmpeg 路径（根据您的实际安装路径修改）
# 示例 Windows 路径：r"C:\ffmpeg\bin\ffmpeg.exe"
# 示例 macOS/Linux 路径："/usr/local/bin/ffmpeg"
# from pydub import AudioSegment
# AudioSegment.converter = r"C:\Path\To\ffmpeg\bin\ffmpeg.exe"

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("skipaudiomaker.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    app = QApplication(sys.argv)
    
    # 设置品牌样式
    try:
        app.setStyleSheet(BrandColors.get_stylesheet())
        BrandFonts.load_fonts()
    except Exception as e:
        logger.error(f"样式加载失败: {str(e)}")
        # 即使样式加载失败也继续运行
        pass
    
    # 创建并显示启动画面
    splash = None
    try:
        if os.path.exists("assets/branding/splash_screen.png"):
            splash_pix = QPixmap("assets/branding/splash_screen.png")
            splash = QSplashScreen(splash_pix)
            splash.show()
            app.processEvents()
    except Exception as e:
        logger.error(f"启动画面加载失败: {str(e)}")
    
    # 初始化主窗口
    try:
        window = MainWindow()
    except Exception as e:
        logger.critical(f"应用初始化失败: {str(e)}")
        QMessageBox.critical(None, "启动错误", f"应用初始化失败:\n{str(e)}")
        sys.exit(1)
    
    # 关闭启动画面并显示主窗口
    if splash:
        splash.finish(window)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()