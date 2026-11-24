'''
MFCC特征提取->注册声纹特征库->余弦相似度比对
'''
import librosa
import numpy as np
from numpy.linalg import norm
import os
class VoiceprintEngine:
    def __init__(self,sr=16000,n_mfcc=13,threshold=1.0,db_path="dataset/voiceprint_db.npz"):
        #sr: 采样率
        #n_mfcc: MFCC 特征维度
        #threshold: 判定为同一个人的相似度阈值（0~1之间，越大越严格）
        self.sr = sr
        self.n_mfcc = n_mfcc
        self.threshold = threshold
        #特征库
        self.feature_database={}
        self.db_path = db_path
        self.load_database()#自动加载特征库
    def extract_feature(self,audio_path):
        y,_ = librosa.load(audio_path,sr=self.sr)
        mfcc = librosa.feature.mfcc(y=y,sr=self.sr,n_mfcc=self.n_mfcc)
        mean_mfcc = np.mean(mfcc,axis=1)
        return mean_mfcc
    def save_database(self):
        if not os.path.exists(os.path.dirname(self.db_path)):
            os.makedirs(os.path.dirname(self.db_path))
        #字典保存为numpy压缩格式
        np.savez(self.db_path,**self.feature_database)
        print(f"特征库保存至{self.db_path}")
    def load_database(self):
        if os.path.exists(self.db_path):
            data=np.load(self.db_path)#转为字典
            self.feature_database={}
            for k in data.files:
                self.feature_database[k] = data[k]
            print(f"特征库从{self.db_path}加载{len(self.feature_database)}个声纹")
        else:
            print("特征库未找到本地存档")
    def register(self,name,audio_path):
        #声纹注册
        try:
            feature = self.extract_feature(audio_path)
            self.feature_database[name] = feature
            print(f"[注册成功] {name} 的声纹已录入特征库。")
            self.save_database()
            return True
        except Exception as e:
            print(f"[注册失败] {name}: {e}")
            return False
    def identify(self, audio_path):
        #声纹识别
        if not self.feature_database:
            print("[特征库为空]")
            return False, None, 0.0
        try:
            test_feature = self.extract_feature(audio_path)
        except Exception as e:
            print(f"[识别失败] 音频读取异常: {e}")
            return False, None, 0.0
        best_match_name = None
        highest_similarity = -1.0
        for name ,db_feature in self.feature_database.items():
            #计算相似度
            #公式：点积/（模长*模长）
            similarity = np.dot(test_feature,db_feature)/(norm(test_feature)*norm(db_feature))
            if similarity > highest_similarity:
                highest_similarity = similarity
                best_match_name = name
        if highest_similarity>=self.threshold:
            return True,best_match_name,highest_similarity
        else:
            return False,None,highest_similarity