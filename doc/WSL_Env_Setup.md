# Linux 嵌入式开发环境配置指南 (WSL2)

## 1. 概述

本文档由嵌入式部署组编写，用于记录在 Windows 11 环境下基于 WSL2 (Ubuntu 22.04) 搭建 OpenCV 摄像头抓拍开发环境的完整流程。本文档解决了 WSL 默认不支持 USB 摄像头、图形界面报错、抓拍绿屏等核心痛点，为后续项目开发及 RK3588 硬件迁移提供环境底座。

## 2. 基础系统与 Python 环境

本项目使用 Miniconda3 管理 Python 环境。经过实测，Python 3.13 在 Linux 下的部分图形库与底层驱动存在兼容性冲突，因此强制指定使用 Python 3.13 建立专属环境。

### 2.1 创建并激活虚拟环境

```bash
# 创建名为 opencv_py313 的环境，指定 Python 版本为 3.13
conda create -n opencv_py313 python=3.13 -y

# 激活环境（执行后终端前缀会变为 (opencv_py313)）
conda activate opencv_py313

# 安装项目核心依赖
pip install opencv-python numpy
```

## 3. USB 摄像头挂载与测试

> **痛点**：WSL 无法直接访问宿主机的 USB 设备，必须借助 usbipd-win 将 Windows 的硬件"转发"进 Linux 子系统。

### 3.1 启动连接摄像头

在 Windows 端，以管理员身份打开 PowerShell（注意：执行 `attach` 时，必须保持 WSL 终端处于开启状态）：

```bash
powershell
# 查看设备列表，假设摄像头的 BUSID 为 1-3
usbipd list

# 将设备挂载到 WSL
usbipd attach -w -b 1-3
#powershell挂在后台
```

### 3.2 在 WSL 中验证硬件

挂载成功后，回到 WSL 终端，验证 USB 设备是否被识别：

```bash
lsusb
```

如果能在列表中看到你的摄像头设备，说明物理连接已打通。

### 3.3 安装 V4L 工具并测试

安装 Video4Linux 工具和摄像头查看器：

```bash
# 安装 v4l-utils 和 guvcview
sudo apt install v4l-utils guvcview -y

# 启动摄像头测试软件
sudo guvcview
```

如果成功弹出窗口并看到画面，说明摄像头驱动和图形界面完全正常。

## 4. 进阶：自定义 WSL 内核编译（解决驱动缺失）

> **痛点**：WSL 默认内核未包含 USB Video Class (UVC) 和 V4L2 驱动，导致代码报错 `can't open camera by index`。

### 4.1 编译步骤
具体参考CSDN博客
1. 下载微软官方 WSL2 内核源码（本项目基于 6.18.58.1 版本）。
```bash
   uname -r#内核版本
```
2. 复制官方配置模板：

```bash
   cp Microsoft/config-wsl .config
```

3. 运行 `make menuconfig`，勾选以下核心驱动：
   - `Device Drivers` → `Multimedia support` → `Filter media drivers`（按 `Y`）
   - `Device Drivers` → `Multimedia support` → `Media device types` → `Cameras and video grabbers`（按 `Y`）
   - **注意**：务必确保 `Microsoft Hyper-V guest support` 相关的 VMBus 等核心项被选中，否则 WSL 将无法启动。

4. 编译内核：

   ```bash
   sudo make -j$(nproc) KCONFIG_CONFIG=.config \
   && sudo make modules_install -j$(nproc) \
   && sudo make install -j$(nproc)
   ```

5. 将生成的镜像复制到 Windows 目录：

   ```bash
   sudo cp arch/x86/boot/bzImage /mnt/c/Users/<UserName>/WSL2/kernel-6.18.58.1
   ```

6. 在 Windows 用户目录下配置 `.wslconfig` 文件：

   ```ini
   [wsl2]
   kernel=C:\\Users\\<UserName>\\WSL2\\kernel-6.18.58.1
   ```

7. 在 PowerShell 执行 `wsl --shutdown` 重启，通过 `uname -r` 验证内核版本。

## 5. 常见报错与避坑记录

### 5.1 设备权限不足 (Permission denied)

**原因**：每次重启 WSL 或重新挂载 USB 后，`/dev/video0` 的权限可能会重置为仅 root 用户可读。

**解决**：

```bash
sudo chmod 666 /dev/video0 /dev/video1
```

### 5.2 OpenCV 抓拍画面全绿或全黑

**原因**：在 Linux 下使用 V4L2 框架调用 USB 摄像头时，如果使用默认参数，很容易出现底层图像格式（如 YUYV）转换异常，或者摄像头刚启动时自动曝光未完成，导致抓拍出来的画面呈纯绿色、全黑或一半绿一半灰。

**解决**：在代码中不仅要增加预热丢帧（让摄像头有时间调整曝光），还必须强制指定分辨率和 MJPG 格式（这种格式在 Linux 下传输最稳定，不容易出现像素格式解析错误）：

```python
import cv2
import time

# 1. 打开摄像头，强制使用 V4L2 后端
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

if cap.isOpened():
    # 2. 强制设置分辨率（如 640x480），对齐硬件输出
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # 3. 强制指定 MJPG 压缩格式（核心解决绿屏的代码）
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

    # 4. 预热丢帧 + 硬件延迟，彻底排空底层缓冲区脏数据
    for _ in range(10):
        cap.read()
    time.sleep(0.5)

    # 5. 正式抓取一帧
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("test.jpg", frame)
        
cap.release()
```

### 5.3 图形界面弹窗报错 ("xcb"错误)
先查看缺少哪些QT库，再补充安装

```bash
sudo apt install libxcb-cursor0 -y
```

## 6. 代码仓库规范说明

- `src/`：存放核心业务模块（如 `camera_module.py`）。
- `test/`：存放独立测试脚本（如 `test_queue_camera.py`）。
- `dataset/`：存放抓拍图像及录音数据（已在 `.gitignore` 中忽略实际文件，仅保留 `.gitkeep` 占位）。
- `doc/`：存放文档（即本文档）。

## 7. 上传Git仓库

上传git仓库

```bash
git add .
git commit -m "docs: 完成 WSL2 环境配置文档及绿屏解决方案整理"
git push github main
git push origin main
```