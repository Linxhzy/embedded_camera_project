'''
单独测试demo
'''
import sys
import os
#解决路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)
from src.camera_module import CameraCapture
from src.voiceprint_engine import VoiceprintEngine
def test_camera_demo():
    print("摄像头抓拍demo")
    camera = CameraCapture(save_dir="dataset/images")
    success,result = camera.capture_single_image()#调用抓拍函数
    if success is True:
        print(f"True:照片在：{result}")
    else:
        print(f"False:原因：{result}")
def test_voiceprint_demo():
    print("声纹识别demo")
    engine = VoiceprintEngine(threshold=0.75)
    audio_path = "dataset/raw/test_audio.wav"
    engine.register("aaa",audio_path)
    is_target,name,score=engine.identify(audio_path)
    if is_target is True:
        print(f"True:目标人物:{name}")
    else:
        print("False:原因")
if __name__=="__main__":
    test_camera_demo()
    test_voiceprint_demo()