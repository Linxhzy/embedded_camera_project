import pyroomacoustics as pra
import numpy as np
import matplotlib.pyplot as plt
print("Pyroomacoustics版本:", pra.__version__)
room_dim = [8,5,3]
room = pra.ShoeBox(room_dim,fs=1600,max_order=3,materials=pra.Material(0.2))
# 添加声源（位置坐标）
room.add_source([2, 2.5, 1.5])
 
# 定义麦克风阵列位置
mic_pos = np.c_[[6, 2.5, 1.5]]  # 单个麦克风
room.add_microphone_array(pra.MicrophoneArray(mic_pos, room.fs))
# 计算房间脉冲响应
room.compute_rir()
 
# 获取脉冲响应
rir = room.rir[0][0]  # 麦克风0，声源0的脉冲响应


# 1. 可视化房间的 3D 布局（包含墙壁、声源、麦克风）
room.plot() 

# 2. 让图像真正弹出来显示
plt.show() 