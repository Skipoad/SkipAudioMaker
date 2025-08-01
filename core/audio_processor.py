import numpy as np
from pydub import AudioSegment
from pydub.effects import speedup
import librosa
import soundfile as sf
from .effects import apply_vibrato, apply_glide
import logging

logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
    
    def load_sample(self, file_path):
        """加载音频样本"""
        try:
            audio = AudioSegment.from_file(file_path)
            if audio.frame_rate != self.sample_rate:
                audio = audio.set_frame_rate(self.sample_rate)
            if audio.channels > 1:
                audio = audio.set_channels(1)  # 转为单声道
            return audio
        except Exception as e:
            logger.error(f"加载样本失败: {str(e)}")
            return AudioSegment.silent(duration=1000)  # 返回静音
    
    def pitch_shift(self, audio, semitones):
        """改变音频音高（移调）"""
        try:
            # 将AudioSegment转换为numpy数组
            samples = np.array(audio.get_array_of_samples())
            
            # 使用librosa进行音高变换
            shifted = librosa.effects.pitch_shift(
                samples.astype(np.float32) / 32768.0,
                sr=self.sample_rate,
                n_steps=semitones
            )
            
            # 转换回AudioSegment
            shifted = (shifted * 32768.0).astype(np.int16)
            return AudioSegment(
                shifted.tobytes(),
                frame_rate=self.sample_rate,
                sample_width=2,
                channels=1
            )
        except Exception as e:
            logger.error(f"音高变换失败: {str(e)}")
            return audio  # 返回原始音频
    
    def render_note(self, note_info, sample, effects=None):
        """渲染单个音符"""
        try:
            # 基本音高调整
            target_pitch = note_info['note']
            original_pitch = 60  # 假设原始样本是C4 (MIDI 60)
            semitones = target_pitch - original_pitch
            processed = self.pitch_shift(sample, semitones)
            
            # 应用效果
            if effects:
                if 'vibrato' in effects:
                    processed = apply_vibrato(processed, 
                                            rate=effects['vibrato']['rate'],
                                            depth=effects['vibrato']['depth'])
                
                if 'glide' in effects:
                    processed = apply_glide(processed, 
                                           start_pitch=effects['glide']['start'],
                                           end_pitch=effects['glide']['end'])
            
            # 调整长度
            target_duration = note_info['duration_sec'] * 1000  # 转换为毫秒
            if len(processed) > target_duration:
                processed = processed[:target_duration]
            elif len(processed) < target_duration:
                # 使用静音填充
                silence = AudioSegment.silent(duration=target_duration - len(processed))
                processed += silence
            
            return processed
        except Exception as e:
            logger.error(f"音符渲染失败: {str(e)}")
            return AudioSegment.silent(duration=note_info['duration_sec'] * 1000)
    
    def render_track(self, notes, samples, effects_map=None):
        """渲染整个音轨"""
        try:
            track = AudioSegment.silent(duration=0)
            timeline = {}
            
            # 创建时间线
            for note in notes:
                start_ms = note['start_sec'] * 1000
                end_ms = note['end_sec'] * 1000
                
                # 获取该音符对应的样本
                sample = samples.get(note['note'], samples.get('default', None))
                if not sample:
                    logger.warning(f"音符 {note['note']} 没有对应的样本，使用静音")
                    sample = AudioSegment.silent(duration=100)
                
                # 获取该音符的效果
                effects = effects_map.get(note['note'], {}) if effects_map else {}
                
                # 渲染音符
                note_audio = self.render_note(note, sample, effects)
                
                # 添加到时间线
                if start_ms not in timeline:
                    timeline[start_ms] = []
                timeline[start_ms].append(note_audio)
            
            # 混合音频
            max_time = max(timeline.keys()) if timeline else 0
            current_time = 0
            
            for time in sorted(timeline.keys()):
                # 确保时间线连续
                if time > current_time:
                    silence = AudioSegment.silent(duration=time - current_time)
                    track += silence
                    current_time = time
                
                # 混合同时发生的音符
                mixed = sum(timeline[time], AudioSegment.silent(duration=0))
                track = track.overlay(mixed, position=time)
                current_time = max(current_time, time + len(mixed))
            
            # 确保总长度足够
            if len(track) < max_time:
                silence = AudioSegment.silent(duration=max_time - len(track))
                track += silence
            
            return track
        except Exception as e:
            logger.error(f"音轨渲染失败: {str(e)}")
            return AudioSegment.silent(duration=5000)  # 返回5秒静音