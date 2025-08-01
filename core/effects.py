import numpy as np
from pydub import AudioSegment
import librosa
import logging

logger = logging.getLogger(__name__)

def apply_vibrato(audio, rate=5, depth=0.5):
    """应用颤音效果"""
    try:
        samples = np.array(audio.get_array_of_samples())
        length = len(samples)
        
        # 创建调制信号
        t = np.arange(length) / audio.frame_rate
        modulation = depth * np.sin(2 * np.pi * rate * t)
        
        # 应用调制
        indices = np.arange(length) + modulation * audio.frame_rate * 0.01
        indices = np.clip(indices, 0, length-1).astype(int)
        
        # 创建新音频
        vibrato_samples = samples[indices].astype(np.int16)
        return AudioSegment(
            vibrato_samples.tobytes(),
            frame_rate=audio.frame_rate,
            sample_width=audio.sample_width,
            channels=audio.channels
        )
    except Exception as e:
        logger.error(f"颤音效果应用失败: {str(e)}")
        return audio

def apply_glide(audio, start_pitch, end_pitch):
    """应用滑音效果"""
    try:
        samples = np.array(audio.get_array_of_samples())
        length = len(samples)
        frame_rate = audio.frame_rate
        
        # 计算每个采样点的音高变化
        semitones = np.linspace(start_pitch, end_pitch, length)
        
        # 应用音高变换
        glided = np.zeros_like(samples, dtype=np.float32)
        
        # 分块处理
        block_size = 1024
        num_blocks = (length + block_size - 1) // block_size
        
        for i in range(num_blocks):
            start_idx = i * block_size
            end_idx = min((i + 1) * block_size, length)
            block_length = end_idx - start_idx
            
            if block_length <= 0:
                continue
                
            # 获取当前块的音高
            block_pitch = np.mean(semitones[start_idx:end_idx])
            
            # 获取当前块的音频数据
            block = samples[start_idx:end_idx].astype(np.float32) / 32768.0
            
            # 使用librosa进行音高变换
            block_shifted = librosa.effects.pitch_shift(
                block, 
                sr=frame_rate, 
                n_steps=block_pitch - 60  # 假设原始为C4
            )
            
            # 应用交叉淡化窗口
            fade_length = min(256, block_length // 2)
            fade_in = np.linspace(0, 1, fade_length)
            fade_out = np.linspace(1, 0, fade_length)
            
            # 应用窗口函数
            if block_length > 2 * fade_length:
                window = np.ones(block_length)
                window[:fade_length] = fade_in
                window[-fade_length:] = fade_out
            else:
                window = np.ones(block_length)
            
            # 混合回主音频
            glided_block = block_shifted * window
            glided[start_idx:end_idx] += (glided_block * 32768).astype(np.int16)
        
        # 创建新音频
        return AudioSegment(
            glided.astype(np.int16).tobytes(),
            frame_rate=frame_rate,
            sample_width=audio.sample_width,
            channels=audio.channels
        )
    except Exception as e:
        logger.error(f"滑音效果应用失败: {str(e)}")
        return audio