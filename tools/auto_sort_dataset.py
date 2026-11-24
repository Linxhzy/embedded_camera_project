import os
import shutil
def auto_sort_dataset():
    raw_dir = "dataset/raw"
    target_base_dir = "dataset/important"
    if not os.path.exists(raw_dir):
        print(f"找不到{raw_dir}")
        return
    if not os.path.exists(target_base_dir):
        os.makedirs(target_base_dir)
    file_count = 0
    for filename in os.listdir(raw_dir):
        if filename.endswith(".wav"):
            file_count+=1
            if "_" in filename:
                speaker_name = filename.split("_")[0]
            else:
                speaker_name = "unknown"
            speaker_dir = os.path.join(target_base_dir,speaker_name)
            if not os.path.exists(speaker_dir):
                os.makedirs(speaker_dir)
                print(f"创建{speaker_dir}")
            source_path = os.path.join(raw_dir,filename)
            target_path = os.path.join(speaker_dir,filename)
            shutil.move(source_path,target_path)
            print(f"移动{filename}->{speaker_dir}")
    if file_count==0:
        print("raw下没有.wav文件")
    else:
        print(f"处理了{file_count}个文件")
if __name__ == "__main__":
    auto_sort_dataset()
