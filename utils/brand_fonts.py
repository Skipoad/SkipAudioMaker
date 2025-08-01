from PyQt5.QtGui import QFont

class BrandFonts:
    @staticmethod
    def load_fonts():
        """加载品牌字体"""
        # 这里简化处理，实际项目中可以加载自定义字体
        # 设置默认字体
        default_font = QFont("Arial", 10)
        return {"default": default_font}