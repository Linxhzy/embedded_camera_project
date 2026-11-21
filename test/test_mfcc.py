import librosa
import librosa.display
import matplotlib.pylab as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
class AudioFeatureExtractor:
    def __init__(self,sr=16000,n_mfcc=13):
     #初始化特征提取器 sr: 采样率，默认 16000 n_mfcc: 提取的 MFCC 维度，默认 13 维
        self.sr = sr
        self.n_mfcc = n_mfcc
    def extract_mfcc(self, audio_path):
        try:
            #加载音频并统一采样率
            y, _ = librosa.load(audio_path, sr=self.sr)
            # 安全检查：防止空音频报错
            if len(y) == 0:
                print(f"文件 {audio_path} 是空")
                return None, None
            #提取 MFCC 特征
            mfcc = librosa.feature.mfcc(y=y, sr=self.sr, n_mfcc=self.n_mfcc)
            return mfcc, y
        except Exception as e:
            print(f"提取特征失败: {e}")
            return None, None
    #可视化
    def plot_mfcc(self,mfcc,title="MFCC声纹特征指纹"):
        if mfcc is None:
            return
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(mfcc, x_axis='time', cmap='viridis')
        plt.colorbar(format='%+2.0f')
        plt.title(title)
        plt.tight_layout()
        plt.show()
if __name__ == "__main__":
    extractor = AudioFeatureExtractor()
    #提取特征
    audio_file = "dataset/raw/test_audio.wav"
    mfcc_features, y_raw = extractor.extract_mfcc(audio_file)
    
    if mfcc_features is not None:
        print(f"原始波形数据形状: {y_raw.shape}")
        print(f"MFCC特征形状: {mfcc_features.shape}")
        #画图
        extractor.plot_mfcc(mfcc_features, title=f"MFCC 特征指纹 [{audio_file}]")