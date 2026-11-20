import os
def check_and_fix_paths():
    ok = True
    print("WSL环境检查...")
    required_dirs=["dataset",
                   "dataset/raw",
                   "dataset/images",
                   "src",
                   "test",
                   "doc"]
    for d in required_dirs:
        if os.path.exists(d):
            print(f"[目录正常]:{d}/")
        else:
            print(f"[缺少目录]:{d}/,正在创建...")
            os.makedirs(d,exist_ok=True)
            if "dataset" in d:#如果是dataset子目录，创建.gitkeep
                open(os.path.join(d,".gitkeep"),"a").close()
    # 2. 检查核心代码文件是否存在（防止误删或重命名）
    required_files = [
        "src/camera_module.py",
        "test/test_record.py",
        "test/test_augment_advanced.py",
        "test/test_lib.py",
        "test/test_queue_camera.py"
    ]

    for f in required_files:
        if os.path.isfile(f):
            print(f"[文件存在]:{f}")
        else:
            print(f"[严重警告:找不到核心文件]:{f}，请检查是否忘记编写或放错位置！")
            ok=False
    print("环境体检完毕:")
    if ok:
        print("环境正常")
    else:
        print("环境异常")
if __name__ == "__main__":
    check_and_fix_paths()
