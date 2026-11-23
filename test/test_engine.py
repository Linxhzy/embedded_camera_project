'''
调用scr/voiceprint_engine.py模拟声音录入->利用余弦相似度对两个声音进行比对
'''
import sys
import os

# 处理路径，引入 src 里的模块
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)
from src.voiceprint_engine import VoiceprintEngine

if __name__ == "__main__":
    engine = VoiceprintEngine()#实例化
    target_audio = "dataset/raw/test_audio.wav"
    unknown_audio = "dataset/raw/test_audio2.wav" 
    
    print("开始声纹注册")
    engine.register("aaa", target_audio)
    print("声纹识别")
    is_match, name, score = engine.identify(unknown_audio)
    print(f"识别结果:")
    print(f"相似度得分: {score:.4f}")
    if is_match:
        print(f"[匹配成功]目标人物是: {name}")
    else:
        print(f"[匹配失败]非目标人物。")