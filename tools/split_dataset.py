import os
import random
import shutil#复制文件
def split_dataset(base_dir="dataset/important",train_ratio=0.8,seed=42):
    #从important获取音频文件，0.8放训练集，随机种子42号
    random.seed(seed)
    train_dir, val_dir = "dataset/train", "dataset/val"#训练集，验证集
    for person in os.listdir(base_dir):
        pdir = os.path.join(base_dir,person)#拼接路径
        if not os.path.isdir(pdir):
            continue#遇到文件就跳过
        all_files = os.listdir(pdir)
        wav_files=[]
        for f in all_files:
            if f.endswith(".wav"):
                wav_files.append(f)
        files = sorted(wav_files)
        #滤出所有wav文件
        if len(files)<2:
            print(f"{person}只有{len(files)}条文件,跳过")
            continue
        random.shuffle(files)#随机打乱
        idx = int(len(files)*train_ratio)#取0.8
        idx = min(idx,len(files)-1)#保证val至少1个
        idx = max(1,idx)#保证train至少1个
        os.makedirs(os.path.join(train_dir, person), exist_ok=True)#创建train
        os.makedirs(os.path.join(val_dir, person), exist_ok=True)#创建val
        for f in files[:idx]:#0到idx-1放train
            shutil.copy(os.path.join(pdir, f), os.path.join(train_dir, person, f))
        for f in files[idx:]:#idx到末尾放val
            shutil.copy(os.path.join(pdir, f), os.path.join(val_dir, person, f))
        print(f"{person}: 训练 {idx} / 验证 {len(files)-idx}")
if __name__=="__main__":
    split_dataset()


