import logging
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout, 
    QComboBox, QDoubleSpinBox, QPushButton, QLabel
)
from PyQt5.QtCore import Qt

logger = logging.getLogger(__name__)

class EffectEditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.current_note = None
        self.effects = {}
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 音符选择
        note_group = QGroupBox("选择音符")
        note_layout = QFormLayout()
        
        self.note_combo = QComboBox()
        self.note_combo.currentIndexChanged.connect(self.note_selected)
        note_layout.addRow("音符:", self.note_combo)
        
        note_group.setLayout(note_layout)
        layout.addWidget(note_group)
        
        # 效果编辑
        effect_group = QGroupBox("效果设置")
        effect_layout = QFormLayout()
        
        # 颤音设置
        effect_layout.addRow(QLabel("颤音设置"))
        self.vibrato_rate = QDoubleSpinBox()
        self.vibrato_rate.setRange(0.1, 20.0)
        self.vibrato_rate.setValue(5.0)
        self.vibrato_rate.setSingleStep(0.5)
        effect_layout.addRow("频率 (Hz):", self.vibrato_rate)
        
        self.vibrato_depth = QDoubleSpinBox()
        self.vibrato_depth.setRange(0.01, 2.0)
        self.vibrato_depth.setValue(0.5)
        self.vibrato_depth.setSingleStep(0.05)
        effect_layout.addRow("深度:", self.vibrato_depth)
        
        # 滑音设置
        effect_layout.addRow(QLabel("滑音设置"))
        self.glide_start = QDoubleSpinBox()
        self.glide_start.setRange(0, 127)
        self.glide_start.setValue(60)
        effect_layout.addRow("起始音高:", self.glide_start)
        
        self.glide_end = QDoubleSpinBox()
        self.glide_end.setRange(0, 127)
        self.glide_end.setValue(60)
        effect_layout.addRow("结束音高:", self.glide_end)
        
        # 应用按钮
        self.apply_button = QPushButton("应用效果")
        self.apply_button.clicked.connect(self.apply_effects)
        effect_layout.addRow(self.apply_button)
        
        effect_group.setLayout(effect_layout)
        layout.addWidget(effect_group)
        
        # 初始化音符列表
        self.update_note_list()
    
    def update_note_list(self):
        """更新音符列表"""
        self.note_combo.clear()
        self.current_note = None  # 重置当前选中的音符
        
        # 检查是否有音符
        if hasattr(self.main_window, 'project') and hasattr(self.main_window.project, 'notes') and self.main_window.project.notes:
            unique_notes = sorted(set(note['note'] for note in self.main_window.project.notes))
            for note in unique_notes:
                self.note_combo.addItem(str(note), note)
            
            # 如果有音符，设置第一个为当前选中的音符
            if unique_notes:
                self.current_note = unique_notes[0]
                self.note_combo.setCurrentIndex(0)  # 选中第一个音符
        else:
            # 没有音符时添加一个占位项
            self.note_combo.addItem("无可用音符", None)
    
    def note_selected(self, index):
        """音符选择变化"""
        if index >= 0:
            note_data = self.note_combo.itemData(index)
            if note_data is not None:  # 确保不是占位项
                self.current_note = note_data
                
                # 加载该音符的已有效果设置
                if self.current_note in self.effects:
                    effects = self.effects[self.current_note]
                    
                    # 加载颤音设置
                    if 'vibrato' in effects:
                        self.vibrato_rate.setValue(effects['vibrato']['rate'])
                        self.vibrato_depth.setValue(effects['vibrato']['depth'])
                    else:
                        self.vibrato_rate.setValue(5.0)  # 恢复默认值
                        self.vibrato_depth.setValue(0.5)
                    
                    # 加载滑音设置
                    if 'glide' in effects:
                        self.glide_start.setValue(effects['glide']['start'])
                        self.glide_end.setValue(effects['glide']['end'])
                    else:
                        self.glide_start.setValue(60)
                        self.glide_end.setValue(60)
    
    def apply_effects(self):
        """应用效果设置到当前音符"""
        if not self.current_note or self.current_note == "无可用音符":
            return
        
        # 创建效果配置
        effects = {}
        
        # 颤音
        if self.vibrato_rate.value() > 0 and self.vibrato_depth.value() > 0:
            effects['vibrato'] = {
                'rate': self.vibrato_rate.value(),
                'depth': self.vibrato_depth.value()
            }
        
        # 滑音
        if self.glide_start.value() != self.glide_end.value():
            effects['glide'] = {
                'start': self.glide_start.value(),
                'end': self.glide_end.value()
            }
        
        # 保存效果
        self.effects[self.current_note] = effects
        self.main_window.statusBar().showMessage(f"效果已应用到音符 {self.current_note}")
    
    def get_effect_map(self):
        """获取效果映射"""
        return self.effects