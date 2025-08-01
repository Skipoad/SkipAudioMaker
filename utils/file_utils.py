import os

def get_audio_files_in_directory(directory):
    """
    获取目录中的所有音频文件
    
    参数:
        directory: 要扫描的目录路径
        
    返回:
        音频文件路径列表
    """
    audio_extensions = ['.wav', '.mp3', '.ogg', '.flac']
    files = []
    for file in os.listdir(directory):
        if any(file.lower().endswith(ext) for ext in audio_extensions):
            files.append(os.path.join(directory, file))
    return files

def ensure_directory_exists(path):
    """
    确保目录存在，如果不存在则创建
    
    参数:
        path: 目录路径
    """
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def get_unique_filename(file_path):
    """
    如果文件已存在，生成唯一的文件名（通过添加数字后缀）
    
    参数:
        file_path: 原始文件路径
        
    返回:
        唯一的文件路径
    """
    if not os.path.exists(file_path):
        return file_path
        
    base, ext = os.path.splitext(file_path)
    counter = 1
    while True:
        new_path = f"{base}_{counter}{ext}"
        if not os.path.exists(new_path):
            return new_path
        counter += 1