import numpy as np
from pydub import AudioSegment

def normalize_audio(audio_segment):
    """
    归一化音频到最大幅度
    
    参数:
        audio_segment: pydub.AudioSegment 对象
        
    返回:
        归一化后的 AudioSegment
    """
    # 计算归一化增益（使最大幅度达到 -0.1 dB）
    change_in_dBFS = -0.1 - audio_segment.dBFS
    return audio_segment.apply_gain(change_in_dBFS)

def mix_audio_segments(segments):
    """
    混合多个音频段
    
    参数:
        segments: AudioSegment 对象列表
        
    返回:
        混合后的 AudioSegment
    """
    if not segments:
        return None
        
    # 找到最长的音频段
    max_duration = max(len(segment) for segment in segments)
    
    # 创建静音基础段
    mixed = AudioSegment.silent(duration=max_duration)
    
    # 混合所有音频段
    for segment in segments:
        # 如果音频段比基础段短，需要填充
        if len(segment) < max_duration:
            segment = segment + AudioSegment.silent(duration=max_duration - len(segment))
        mixed = mixed.overlay(segment)
    
    return mixed

def calculate_rms(audio_segment):
    """
    计算音频的 RMS（均方根）值
    
    参数:
        audio_segment: pydub.AudioSegment 对象
        
    返回:
        RMS 值 (0.0 - 1.0)
    """
    samples = np.array(audio_segment.get_array_of_samples())
    # 转换为浮点数并归一化到 [-1, 1] 范围
    samples = samples.astype(np.float32) / (2**(8*audio_segment.sample_width - 1))
    return np.sqrt(np.mean(np.square(samples)))

def fade_in_out(audio_segment, fade_duration=100):
    """
    为音频段添加淡入淡出效果
    
    参数:
        audio_segment: pydub.AudioSegment 对象
        fade_duration: 淡入淡出时长（毫秒）
        
    返回:
        添加淡入淡出后的 AudioSegment
    """
    # 确保淡入淡出时间不超过音频长度的一半
    fade_duration = min(fade_duration, len(audio_segment) // 2)
    
    # 应用淡入淡出
    return audio_segment.fade_in(fade_duration).fade_out(fade_duration)