'''
利用queue实现多线程抓拍
'''
import os
import sys
import time
import threading
import queue
# 处理路径问题，确保能引入 src 里的模块
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)
# 导入抓拍模块
from src.camera_module import CameraCapture
task_queue = queue.Queue()
camera = CameraCapture(save_dir="dataset/images")
#消费者
def camera_worker():
    print("[抓拍线程]:启动...")
    while True:
        signal = task_queue.get()
        if signal =="EXIT":
            print("[抓拍线程]:退出")
            break
        if signal =="CAPTURE":
            print("[抓拍线程]:收到抓拍信号，拍摄")
            success,result = camera.capture_single_image()
            if success:
                print(f"[抓拍线程]:保存成功{result}")
            else:
                print(f"[抓拍线程]:抓拍失败{result}")
    task_queue.task_done()
#主程序
def main():
    t = threading.Thread(target=camera_worker,daemon = True)
    t.start()
    print("[主程序]:模拟音频信号...")
    try:
        for i in range(3):
            time.sleep(3)
            print(f"[主程序]:第{i+1}次音频信号,发送抓拍信号")
            task_queue.put("CAPTURE")#入队
    except:
        print("程序中断")
    finally:
        print("退出系统...")
        task_queue.put("EXIT")
        t.join()
        print("系统关闭")
if __name__ == "__main__":
    main()

