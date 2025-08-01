"""
SkipAudioMaker 核心模块
包含 MIDI 处理、音频处理、效果应用等功能
"""
from .midi_processor import MidiProcessor
from .audio_processor import AudioProcessor
from .effects import apply_vibrato, apply_glide
from .project import Project

__all__ = ['MidiProcessor', 'AudioProcessor', 'apply_vibrato', 'apply_glide', 'Project']