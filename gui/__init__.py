"""
SkipAudioMaker 图形用户界面模块
包含主窗口、钢琴卷帘视图、样本库管理等功能
"""
from .main_window import MainWindow
from .piano_roll import PianoRollWidget
from .sample_library import SampleLibraryWidget
from .effect_editor import EffectEditorWidget

__all__ = ['MainWindow', 'PianoRollWidget', 'SampleLibraryWidget', 'EffectEditorWidget']