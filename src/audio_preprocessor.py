import librosa
import numpy as np
class AudioPreprocessor:
    def __init__(self,sr=16000,target_duration=3.0,top_db=20):
        self.sr = sr#采样率16000
        self.target_duration = target_duration#目标时长3s
        self.top_db = top_db#低于多少db算静音
    def process(self,file_path):
        try:
            y,_ = librosa.load(file_path,sr = self.sr)#统一采样率
            y_trimmed,_ = librosa.effects.trim(y,top_db=self.top_db)#静音切除
            target_length = int(self.target_duration*self.sr)
            if len(y_trimmed)>target_length:
                y_final = y_trimmed[:target_length]#从头开始
            else:
                padding = target_length-len(y_trimmed)
                y_final = np.pad(y_trimmed,(0,padding),'constant')#np.pad(0,a)是前面补0个，后面补a个，constant是常数，默认补0
            return y_final
        except Exception as e:
            print("[预处理失败]{file_path}:{e}")
            return None


#测试代码
'''
if __name__ == "__main__":
    print("开始测试音频预处理器...")
    
    # 实例化预处理器（设定目标 3 秒）
    preprocessor = AudioPreprocessor(target_duration=3.0)
    
    # 拿你手头的测试音频
    test_file = "dataset/raw/test_audio.wav"
    
    import librosa
    try:
        # 1. 看看原音频多长
        y_orig, sr = librosa.load(test_file, sr=16000)
        print(f"原音频长度: {len(y_orig)} 个数据点 (约 {len(y_orig)/sr:.2f} 秒)")
        
        # 2. 调用你的处理函数
        y_processed = preprocessor.process(test_file)
        
        # 3. 看看处理后多长
        if y_processed is not None:
            print(f"处理后长度: {len(y_processed)} 个数据点")
            
            # 4. 验证是否完美对齐 3 秒(48000个点)
            expected_length = 3.0 * 16000
            if len(y_processed) == expected_length:
                print("完美！切片/补齐逻辑正常。")
            else:
                print("失败了，长度没有对齐。")
                
    except Exception as e:
        print(f"测试出错: {e}")
'''


