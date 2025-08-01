import mido
from collections import defaultdict
import numpy as np

class MidiProcessor:
    def __init__(self):
        self.notes = defaultdict(list)
        self.tempo = 500000  # 默认tempo (120 BPM)
        self.max_time = 0  # 添加最大时间跟踪

    def load_midi(self, file_path):
        """加载并解析MIDI文件"""
        self.notes.clear()
        self.max_time = 0  # 重置最大时间
        try:
            mid = mido.MidiFile(file_path)
            ticks_per_beat = mid.ticks_per_beat
            
            # 解析MIDI消息
            current_time = 0
            for track in mid.tracks:
                for msg in track:
                    current_time += msg.time
                    self.max_time = max(self.max_time, current_time)  # 更新最大时间
                    
                    # 记录速度变化
                    if msg.type == 'set_tempo':
                        self.tempo = msg.tempo
                    
                    # 记录音符
                    if msg.type == 'note_on' and msg.velocity > 0:
                        note_info = {
                            'note': msg.note,
                            'velocity': msg.velocity,
                            'start': current_time,
                            'end': None,
                            'channel': msg.channel
                        }
                        self.notes[msg.note].append(note_info)
                    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                        # 查找匹配的note_on
                        for note in self.notes[msg.note]:
                            # 添加额外检查确保匹配正确的音符
                            if (isinstance(note, dict) and 
                                note['end'] is None and 
                                note['channel'] == msg.channel and
                                note['start'] <= current_time):
                                note['end'] = current_time
                                break
            
            # 计算实际时间（秒）
            self._convert_to_seconds(ticks_per_beat)
            
            return self.notes
        except Exception as e:
            raise RuntimeError(f"MIDI文件解析失败: {str(e)}")

    def _convert_to_seconds(self, ticks_per_beat):
        """将tick时间转换为秒"""
        microseconds_per_tick = self.tempo / ticks_per_beat
        
        for note_list in self.notes.values():
            for note in note_list:
                # 跳过非字典项（防止'int' object is not subscriptable错误）
                if not isinstance(note, dict):
                    continue
                
                # 处理未结束的音符（没有匹配note_off）
                if note['end'] is None:
                    note['end'] = self.max_time  # 使用文件最大时间作为结束
                
                note['start_sec'] = note['start'] * microseconds_per_tick / 1_000_000
                note['duration_sec'] = (note['end'] - note['start']) * microseconds_per_tick / 1_000_000
                note['end_sec'] = note['start_sec'] + note['duration_sec']
    
    def get_note_list(self):
        """获取所有音符的列表"""
        all_notes = []
        for note_list in self.notes.values():
            # 过滤掉非字典项
            all_notes.extend([n for n in note_list if isinstance(n, dict)])
        return sorted(all_notes, key=lambda x: x['start_sec'])