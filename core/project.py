class Project:
    def __init__(self):
        self.notes = []
        self.samples = {}  # 音符到样本路径的映射
        self.default_sample = None
        self.effects = {}  # 音符到效果设置的映射
    
    def set_notes(self, notes):
        """设置音符数据"""
        self.notes = notes
    
    def get_note_list(self):
        """获取音符列表"""
        return self.notes if hasattr(self, 'notes') else []
    
    def add_sample(self, note_name, file_path):
        """添加样本"""
        self.samples[note_name] = file_path
        if not self.default_sample:
            self.default_sample = file_path
    
    def remove_sample(self, note_name):
        """移除样本"""
        if note_name in self.samples:
            del self.samples[note_name]
            if self.default_sample == self.samples[note_name]:
                self.default_sample = next(iter(self.samples.values()), None)
    
    def get_sample_path(self, note_name):
        """获取样本路径"""
        return self.samples.get(note_name, self.default_sample)