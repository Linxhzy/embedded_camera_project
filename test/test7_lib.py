import librosa
import librosa.display
import numpy as np
import matplotlib.pylab as plt
Audio_File = "dataset//augmented_audio.wav"
# 设置中文字体（WSL Ubuntu 默认一般有文泉驿或 Noto Sans CJK）
plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK JP', 'SimHei', 'Microsoft YaHei']
# 解决负号 '-' 显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False 
audio_file = Audio_File
y,sr = librosa.load(audio_file,sr=16000)
print(f"采样率{sr}")
print(f"音频数据形状{y.shape}")
print(f"数据类型{y.dtype}")
duration = len(y)/sr #采样点/采样率
print(f"音频时长{duration}")
max_amp = np.max(np.abs(y))
print(f"最大振幅{max_amp:.4f}")
plt.figure(figsize=(12,8))
plt.subplot(2,1,1)
librosa.display.waveshow(y,sr=sr,color="blue")
plt.title(f"波形图(时域)[{audio_file}]")
plt.xlabel("时间(s)")
plt.ylabel("幅度")
plt.subplot(2,1,2)
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)),ref=np.max)
librosa.display.specshow(D,sr=sr,x_axis="time",y_axis="log",cmap="magma")
plt.colorbar(format='%+2.0f db')
plt.title(f"频谱图[{audio_file}]")
plt.xlabel("时间(s)")
plt.ylabel("频率(Hz)")
plt.tight_layout()
plt.show()


