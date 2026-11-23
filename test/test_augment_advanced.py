'''
基于pyroomacoustics的叠加房间混响和高斯噪声
'''
import numpy as np
import pyroomacoustics as pra
import librosa
import soundfile as sf
import os
audio_file="dataset/raw/test_audio.wav"
y,sr =librosa.load(audio_file,sr=16000)
room_dim = [8,6,3]#房间 长8宽6高3
rt60 = 0.6#混响时间
e_absorption,max_order = pra.inverse_sabine(rt60,room_dim)#根据混响时间计算吸音系数
room = pra.ShoeBox(room_dim,fs=sr,materials=pra.Material(e_absorption),max_order=max_order)
room.add_source([1,1,1],signal=y)#声源
mic_locs=np.array([[7],[5],[1.5]])
room.add_microphone_array(mic_locs)#麦克风
room.simulate()#启动
# 提取带混响的音频
reverb_audio = room.mic_array.signals[0, :]
# 叠加高斯白噪声
target_snr = 10.0# 目标信噪比 (SNR = 10 dB)
signal_power = np.mean(reverb_audio ** 2)# 计算原音频的能量
noise_power = signal_power / (10 ** (target_snr / 10))# 根据 SNR 计算需要的噪声能量
noise = np.random.randn(len(reverb_audio)) * np.sqrt(noise_power)# 随机生成符合能量的高斯白噪声
final_audio = reverb_audio + noise# 最终音频 = 混响音频 + 噪声
# 保存结果
output_file = "dataset/raw/augmented_audio.wav"
sf.write(output_file, final_audio, sr)
print(f"混响及噪声添加完成已保存至: {output_file}")



