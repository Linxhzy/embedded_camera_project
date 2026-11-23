# 嵌入式部署组核心模块接口定义文档 (v1.0)

## 1. 文档说明
为了确保多线程队列（Queue）通信的稳定性，所有触发信号（如：是否抓拍、是否为目标人物）必须统一返回标准布尔值（`True` / `False`）。

---

## 2. 摄像头抓拍模块 (`CameraCapture`)
**代码路径**：`src/camera_module.py`

### 2.1 单次抓拍接口
*   **方法名**：`capture_single_image(self)`
*   **入参**：无（初始化时已通过 `CameraCapture(save_dir="dataset/images")` 绑定保存目录）。
*   **返回值**：元组 `(bool, str)`
    *   `bool` (**核心信号**)：抓拍并保存成功返回 `True`，失败返回 `False`。
    *   `str`：成功时返回图片的保存路径；失败时返回错误原因。
*   **代码示例**：
    ```python
    success, file_path = camera.capture_single_image()
    if success is True:
        print(f"抓拍成功，存至：{file_path}")
    ```

---

## 3. 声纹识别模块 (`VoiceprintEngine`)
**代码路径**：`src/voiceprint_engine.py`

### 3.1 声纹注册接口
*   **方法名**：`register(self, name, audio_path)`
*   **入参**：
    *   `name` (str): 目标人物的标签名（如 "zhangsan"）。
    *   `audio_path` (str): 用于注册的干净音频文件路径。
*   **返回值**：`bool`（注册成功 `True`，读取失败或异常 `False`）。

### 3.2 声纹识别接口
*   **方法名**：`identify(self, audio_path)`
*   **入参**：
    *   `audio_path` (str): 待识别的音频文件路径。
*   **返回值**：元组 `(bool, str, float)`
    *   `bool` (**核心信号**)：识别为目标人物返回 `True`，非目标/静音/异常返回 `False`。
    *   `str`：匹配成功时返回人物标签名，失败时返回 `None`。
    *   `float`：余弦相似度得分（0.0 ~ 1.0）。
*   **代码示例**：
    ```python
    is_target, name, score = engine.identify("dataset/raw/test.wav")
    if is_target is True:
        # 触发后续抓拍逻辑
        queue.put("CAPTURE")
    ```

---