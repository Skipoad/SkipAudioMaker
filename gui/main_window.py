#main_window.py
import os
import sys
import logging
from PyQt5.QtWidgets import (
    QMainWindow, QFileDialog, QMessageBox, QAction, QDockWidget, QTabWidget, 
    QStatusBar, QLabel, QDialog, QVBoxLayout, QApplication
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap
from .piano_roll import PianoRollWidget
from .sample_library import SampleLibraryWidget
from .effect_editor import EffectEditorWidget
from core.midi_processor import MidiProcessor
from core.audio_processor import AudioProcessor
from core.project import Project
import tempfile
import platform

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SkipAudioMaker Beta 1.0")
        self.setGeometry(100, 100, 1200, 800)
        
        # 初始化项目
        self.project = Project()
        self.midi_processor = MidiProcessor()
        self.audio_processor = AudioProcessor()
        self.current_audio_path = None
        
        # 创建UI
        self.init_ui()
        self.init_menu()
        self.init_toolbar()
        self.init_statusbar()
        
        # 加载默认设置
        self.load_default_samples()
        
        # 设置图标
        self.setWindowIcon(QIcon('assets/icons/app_icon.png'))
    
    def init_ui(self):
        """初始化主界面"""
        # 创建中心部件 - 钢琴卷帘
        self.piano_roll = PianoRollWidget(self)
        self.setCentralWidget(self.piano_roll)
        
        # 创建停靠窗口
        self.init_docks()
    
    def init_docks(self):
        """初始化停靠窗口"""
        # 样本库
        self.sample_lib_dock = QDockWidget("样本库", self)
        self.sample_lib_widget = SampleLibraryWidget(self)
        self.sample_lib_dock.setWidget(self.sample_lib_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.sample_lib_dock)
        
        # 效果编辑器
        self.effect_editor_dock = QDockWidget("效果编辑器", self)
        self.effect_editor_widget = EffectEditorWidget(self)
        self.effect_editor_dock.setWidget(self.effect_editor_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.effect_editor_dock)
    
    def init_menu(self):
        """初始化菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        # 导入MIDI
        import_midi_action = QAction('导入MIDI', self)
        import_midi_action.triggered.connect(self.import_midi)
        file_menu.addAction(import_midi_action)
        
        # 导出音频
        export_audio_action = QAction('导出音频', self)
        export_audio_action.triggered.connect(self.export_audio)
        file_menu.addAction(export_audio_action)
        
        # 退出
        exit_action = QAction('退出', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu('编辑')
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助')
        about_action = QAction('关于', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def init_toolbar(self):
        """初始化工具栏"""
        toolbar = self.addToolBar('工具')
        
        # 导入MIDI按钮
        import_midi_action = QAction(QIcon('assets/icons/toolbar/import_midi.png'), '导入MIDI', self)
        import_midi_action.triggered.connect(self.import_midi)
        toolbar.addAction(import_midi_action)
        
        # 播放按钮
        play_action = QAction(QIcon('assets/icons/toolbar/play.png'), '播放', self)
        play_action.triggered.connect(self.play_audio)
        toolbar.addAction(play_action)
        
        # 停止按钮
        stop_action = QAction(QIcon('assets/icons/toolbar/stop.png'), '停止', self)
        stop_action.triggered.connect(self.stop_audio)
        toolbar.addAction(stop_action)
        
        # 导出按钮
        export_action = QAction(QIcon('assets/icons/toolbar/export.png'), '导出', self)
        export_action.triggered.connect(self.export_audio)
        toolbar.addAction(export_action)
    
    def init_statusbar(self):
        """初始化状态栏"""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("就绪")
        
        # 添加内存状态指示器
        self.memory_label = QLabel()
        self.statusbar.addPermanentWidget(self.memory_label)
        
        # 定时更新内存状态
        self.memory_timer = QTimer(self)
        self.memory_timer.timeout.connect(self.update_memory_status)
        self.memory_timer.start(5000)  # 每5秒更新一次
    
    def update_memory_status(self):
        """更新内存状态显示"""
        try:
            if platform.system() == 'Windows':
                import psutil
                memory = psutil.virtual_memory()
                self.memory_label.setText(f"内存: {memory.percent}%")
            else:
                self.memory_label.setText("")
        except:
            self.memory_label.setText("")
    
    def load_default_samples(self):
        """加载默认样本"""
        default_dir = "assets/default_samples/"
        if os.path.exists(default_dir):
            for file in os.listdir(default_dir):
                if file.endswith((".wav", ".mp3", ".ogg")):
                    note_name = os.path.splitext(file)[0]
                    file_path = os.path.join(default_dir, file)
                    self.project.add_sample(note_name, file_path)
                    self.sample_lib_widget.add_sample(note_name, file_path)
    
    def import_midi(self):
        """导入MIDI文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入MIDI文件", "", "MIDI文件 (*.mid *.midi)"
        )
        
        if file_path:
            try:
                self.statusbar.showMessage(f"正在加载: {file_path}")
                
                # 修复点1: 确保正确处理返回的notes数据结构
                # 使用get_note_list()获取排序后的音符列表
                self.midi_processor.load_midi(file_path)
                notes = self.midi_processor.get_note_list()
                
                self.project.set_notes(notes)
                
                # 修复点2: 添加额外检查确保notes是列表
                if not isinstance(notes, list):
                    logger.warning(f"Unexpected notes type: {type(notes)}")
                    notes = []
                
                self.piano_roll.load_notes(notes)
                self.effect_editor_widget.update_note_list()
                self.statusbar.showMessage(f"成功加载: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "导入错误", f"无法导入MIDI文件:\n{str(e)}")
                logger.error(f"MIDI导入失败: {str(e)}", exc_info=True)  # 添加详细错误信息
    
    def play_audio(self):
        """播放音频"""
        if not self.project.notes:
            QMessageBox.warning(self, "播放错误", "没有可播放的音符")
            return
        
        try:
            self.statusbar.showMessage("正在渲染音频...")
            QApplication.processEvents()  # 更新UI
            
            # 获取样本映射
            sample_map = self.sample_lib_widget.get_sample_map(self.audio_processor)
            
            # 获取效果映射
            effect_map = self.effect_editor_widget.get_effect_map()
            
            # 渲染音轨
            track = self.audio_processor.render_track(
                self.project.get_note_list(),
                sample_map,
                effect_map
            )
            
            # 保存临时文件并播放
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmpfile:
                self.current_audio_path = tmpfile.name
                track.export(self.current_audio_path, format="wav")
            
            self.statusbar.showMessage("正在播放...按停止键结束播放")
            # 在实际应用中，这里应该使用QMediaPlayer播放音频
            # 这里简化处理，使用系统默认播放器
            if platform.system() == 'Windows':
                os.startfile(self.current_audio_path)
            elif platform.system() == 'Darwin':
                os.system(f"afplay '{self.current_audio_path}' &")
            else:
                os.system(f"aplay '{self.current_audio_path}' &")
                
        except Exception as e:
            QMessageBox.critical(self, "渲染错误", f"音频渲染失败:\n{str(e)}")
            logger.error(f"音频渲染失败: {str(e)}", exc_info=True)  # 添加详细错误信息
        finally:
            self.statusbar.showMessage("就绪")
    
    def stop_audio(self):
        """停止播放"""
        # 在实际应用中需要停止播放器
        # 这里简化处理，只更新状态
        self.statusbar.showMessage("播放停止")
    
    def export_audio(self):
        """导出音频文件"""
        if not self.project.notes:
            QMessageBox.warning(self, "导出错误", "没有可导出的音符")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出音频", "", "音频文件 (*.wav)"
        )
        
        if file_path:
            try:
                if not file_path.endswith('.wav'):
                    file_path += '.wav'
                
                self.statusbar.showMessage("正在渲染音频...")
                QApplication.processEvents()  # 更新UI
                
                # 获取样本映射
                sample_map = self.sample_lib_widget.get_sample_map(self.audio_processor)
                
                # 获取效果映射
                effect_map = self.effect_editor_widget.get_effect_map()
                
                # 渲染音轨
                track = self.audio_processor.render_track(
                    self.project.get_note_list(),
                    sample_map,
                    effect_map
                )
                
                # 导出音频
                track.export(file_path, format="wav")
                self.statusbar.showMessage(f"成功导出: {os.path.basename(file_path)}")
                
            except Exception as e:
                QMessageBox.critical(self, "导出错误", f"导出失败:\n{str(e)}")
                logger.error(f"音频导出失败: {str(e)}", exc_info=True)  # 添加详细错误信息
            finally:
                self.statusbar.showMessage("就绪")
    
    def show_about(self):
        """显示关于对话框"""
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("关于 SkipAudioMaker")
        about_dialog.setFixedSize(400, 400)
        
        layout = QVBoxLayout()
        
        # Logo展示
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        if os.path.exists("assets/branding/about_logo.png"):
            logo_pixmap = QPixmap("assets/branding/about_logo.png").scaled(200, 200, Qt.KeepAspectRatio)
            logo_label.setPixmap(logo_pixmap)
        else:
            logo_label.setText("SkipAudioMaker")
            logo_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #3498DB;")
        
        layout.addWidget(logo_label)
        
        # 应用信息
        info_text = QLabel(
            "<h2>SkipAudioMaker v1.0</h2>"
            "<p>一个强大的鬼畜音频制作工具</p>"
            "<p>© 2025 保留所有权利</p>"
        )
        info_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_text)
        
        about_dialog.setLayout(layout)
        about_dialog.exec_()