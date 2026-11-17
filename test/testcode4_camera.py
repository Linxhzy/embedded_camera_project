import sys
import os
import time
'''
把上一级目录(code文件夹)加入系统路径
这样 test 文件夹里的代码才能 import 到 code 里的模块
'''
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.camera_module import CameraCapture
def main():
    print("启动调用抓拍模块")
    camera = CameraCapture(save_dir="dataset")
    for i in range(3):
        print(f"第{i+1}张")
        success,result = camera.capture_single_image()
        if success:
            print(f"Success:{result}")
        else:
            print(f"Faild:{result}")
        time.sleep(1)
main()
