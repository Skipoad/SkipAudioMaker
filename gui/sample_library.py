import os
import logging
from PyQt5.QtWidgets import (
    QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QFileDialog, QListWidgetItem, QMessageBox, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

logger = logging.getLogger(__name__)

class SampleLibraryWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("样本库")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title_label)
        
        # 样本列表
        self.sample_list = QListWidget()
        self.sample_list.setSelectionMode(QListWidget.SingleSelection)
        layout.addWidget(self.sample_list)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        # 添加样本按钮
        self.add_button = QPushButton("添加样本")
        self.add_button.setIcon(QIcon('assets/icons/toolbar/import_midi.png'))
        self.add_button.clicked.connect(self.add_sample)
        button_layout.addWidget(self.add_button)
        
        # 移除样本按钮
        self.remove_button = QPushButton("移除")
        self.remove_button.setIcon(QIcon('assets/icons/toolbar/remove.png'))
        self.remove_button.clicked.connect(self.remove_sample)
        button_layout.addWidget(self.remove_button)
        
        layout.addLayout(button_layout)
    
    def add_sample(self, note_name=None, file_path=None):
        """添加样本到库中"""
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "选择音频样本", "", "音频文件 (*.wav *.mp3 *.ogg)"
            )
        
        if file_path:
            # 获取音符名称
            if not note_name:
                base_name = os.path.splitext(os.path.basename(file_path))[0]
            else:
                base_name = note_name
            
            # 添加到项目
            self.main_window.project.add_sample(base_name, file_path)
            
            # 添加到列表
            item = QListWidgetItem(base_name)
            item.setData(Qt.UserRole, file_path)
            self.sample_list.addItem(item)
    
    def remove_sample(self):
        """从库中移除样本"""
        selected = self.sample_list.currentRow()
        if selected >= 0:
            item = self.sample_list.takeItem(selected)
            note_name = item.text()
            self.main_window.project.remove_sample(note_name)
    
    def get_sample_map(self, audio_processor):
        """获取音符到样本的映射"""
        sample_map = {}
        for i in range(self.sample_list.count()):
            item = self.sample_list.item(i)
            note_name = item.text()
            file_path = item.data(Qt.UserRole)
            sample_map[note_name] = audio_processor.load_sample(file_path)
        
        # 添加默认样本
        if 'default' not in sample_map and self.main_window.project.default_sample:
            sample_map['default'] = audio_processor.load_sample(
                self.main_window.project.default_sample
            )
        
        return sample_map