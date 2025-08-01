import logging
from PyQt5.QtWidgets import (
    QWidget, QScrollArea, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem
)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QPainter, QPen, QBrush, QFont

logger = logging.getLogger(__name__)

class PianoRollWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.notes = []
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        # 创建图形视图
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        
        scroll_area.setWidget(self.graphics_view)
        layout.addWidget(scroll_area)
    
    def load_notes(self, notes):
        """加载音符数据"""
        self.notes = notes
        self.scene.clear()
        
        if not notes:
            return
        
        # 计算时间范围
        min_time = min(note['start_sec'] for note in self.notes)
        max_time = max(note['end_sec'] for note in self.notes)
        time_range = max_time - min_time
        
        # 计算音高范围
        min_note = min(note['note'] for note in self.notes)
        max_note = max(note['note'] for note in self.notes)
        note_range = max_note - min_note + 1
        
        # 设置场景大小
        self.scene.setSceneRect(0, 0, time_range * 200 + 100, note_range * 30 + 50)
        
        # 绘制网格
        self.draw_grid(min_time, max_time, min_note, max_note)
        
        # 绘制音符
        for note in self.notes:
            # 计算位置和大小
            x = (note['start_sec'] - min_time) * 200
            y = (max_note - note['note']) * 30
            width = (note['end_sec'] - note['start_sec']) * 200
            height = 28
            
            # 创建矩形项
            rect = QGraphicsRectItem(x, y, width, height)
            rect.setBrush(QColor(70, 130, 180))  # 钢蓝色
            rect.setPen(QPen(Qt.black, 1))
            self.scene.addItem(rect)
            
            # 添加标签
            note_name = self.get_note_name(note['note'])
            
            # 仅在音符足够宽时显示标签
            if width > 30:
                text = self.scene.addText(f"{note_name}")
                text.setPos(x + 5, y + 5)
                text.setDefaultTextColor(Qt.white)
    
    def draw_grid(self, min_time, max_time, min_note, max_note):
        """绘制钢琴卷帘网格"""
        # 计算参数
        time_range = max_time - min_time
        note_range = max_note - min_note + 1
        
        # 绘制时间网格
        for t in range(0, int(time_range) + 1):
            x = t * 200
            self.scene.addLine(x, 0, x, note_range * 30, QPen(QColor(100, 100, 100, 100)))
            time_label = self.scene.addText(f"{t}s")
            time_label.setPos(x, note_range * 30 + 5)
        
        # 绘制音符网格
        for note in range(min_note, max_note + 1):
            y = (max_note - note) * 30
            self.scene.addLine(0, y, time_range * 200, y, QPen(QColor(100, 100, 100, 50)))
            
            # 添加音符标签
            note_label = self.scene.addText(self.get_note_name(note))
            note_label.setPos(time_range * 200 + 10, y)
    
    def get_note_name(self, midi_note):
        """将MIDI音符编号转换为音名"""
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = midi_note // 12 - 1
        note_index = midi_note % 12
        return f"{notes[note_index]}{octave}"