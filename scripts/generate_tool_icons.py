import os
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import Qt

def generate_icon(text, size=32, bg_color=(70, 130, 180), text_color=(255, 255, 255)):
    """生成简单文字图标"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # 绘制背景
    painter.setBrush(QColor(*bg_color))
    painter.drawRoundedRect(0, 0, size, size, 5, 5)
    
    # 添加文字
    painter.setPen(QColor(*text_color))
    painter.setFont(QFont("Arial", size//2))
    painter.drawText(pixmap.rect(), Qt.AlignCenter, text)
    
    painter.end()
    return QIcon(pixmap)

# 创建工具栏图标目录
os.makedirs("assets/icons/toolbar", exist_ok=True)

# 生成常用工具图标
icons = {
    "import_midi": ("IM", (70, 130, 180)),      # 导入MIDI
    "play": (">", (50, 180, 100)),             # 播放
    "stop": ("■", (200, 50, 50)),              # 停止
    "export": ("E", (180, 130, 50)),           # 导出
    "settings": ("⚙", (120, 100, 180)),        # 设置
    "help": ("?", (150, 100, 200)),            # 帮助
    "remove": ("X", (200, 50, 50))             # 删除
}

for name, (text, color) in icons.items():
    icon = generate_icon(text, bg_color=color)
    icon_path = f"assets/icons/toolbar/{name}.png"
    icon.pixmap(32, 32).save(icon_path)
    print(f"已生成图标: {icon_path}")