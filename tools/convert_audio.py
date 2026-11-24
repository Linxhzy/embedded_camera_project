'''
mp3->wav
'''
import os
from pydub import AudioSegment

# 1. 设置你的文件夹路径（注意前面加个 r，防止路径里的斜杠报错）
folder_path = r"dataset/raw" 

def convert_mp3_to_wav(folder):
    if not os.path.exists(folder):
        print(f"找不到文件夹：{folder}")
        return

    # 遍历文件夹内的所有文件
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        # 清理 Windows 产生的垃圾文件 (Zone.Identifier 和 ~ 临时文件)
        if "Zone.Identifier" in filename or filename.endswith("~"):
            try:
                os.remove(file_path)
                print(f"已清理垃圾文件: {filename}")
            except Exception as e:
                print(f"清理失败 {filename}: {e}")
            continue

        # 处理 MP3 转换
        if filename.lower().endswith(".mp3"):
            print(f"正在转换: {filename} ...")
            try:
                # 读取 MP3
                audio = AudioSegment.from_mp3(file_path)
                # 构造新的 WAV 文件名
                wav_filename = filename[:-4] + ".wav"
                wav_path = os.path.join(folder, wav_filename)
                
                # 导出为 WAV (16-bit PCM，兼容性最好)
                audio.export(wav_path, format="wav")
                print(f"转换成功: {wav_filename}")
                
                # 【可选】转换成功后，是否删除原来的 MP3？
                # 如果你确定不需要原文件了，取消下面这行的注释：
                os.remove(file_path)
                
            except Exception as e:
                print(f"转换失败 {filename}: {e}")

if __name__ == "__main__":
    print("开始处理音频文件...")
    convert_mp3_to_wav(folder_path)
    print("全部处理完成！")