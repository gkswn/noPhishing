import random
import pandas as pd
import numpy as np
import os
import torch

import load_data
import preprocessing

from sklearn.model_selection import StratifiedKFold

from xgboost import XGBClassifier

from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score

import pickle


SEED = 42


def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True

seed_everything(SEED) # Seed 고정


print('=====================Start=====================')


# 데이터 불러오기
train_X, train_y = load_data.dataload()
train_X, train_y = pd.DataFrame(train_X), pd.DataFrame(train_y)



# 데이터 전처리 정의
def preprocess(train_X):

    stopword = preprocessing.make_stopword()
    print("Complete make Stopword List")
    train_X = preprocessing.drop_na(train_X) # 결측치 제거
    print('Complete Drop Null')
    train_X = preprocessing.del_specific(train_X) # 특수기호 제거
    print('Complete Delete Special Symbol')
    train_X['txt'] = train_X['txt'].apply(lambda x : preprocessing.tokenize(x)) # 토큰화
    print('Complete Tokenize')
    train_X['txt'] = train_X['txt'].apply(lambda x : preprocessing.del_stopword(x, stopword)) # 불용어 제거
    print('Complete Delete Stopword')

    return train_X


# train 정의
def train(train_df_X, train_df_y):

    best_F1  = 0
    best_ac = 0

    skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

    for train_idx, test_idx in skf.split(train_df_X, train_df_y):
        # print('TRAIN: ', train_idx, 'TEST: ', test_idx)


        # Data Split!
        train_X, train_y = train_df_X.iloc[train_idx], train_df_y.iloc[train_idx]
        valid_X, valid_y = train_df_X.iloc[test_idx], train_df_y.iloc[test_idx]

        train_X , train_y = pd.DataFrame(train_X), pd.DataFrame(train_y)
        valid_X, valid_y = pd.DataFrame(valid_X), pd.DataFrame(valid_y)


        # Preprocessing!
        train_X = preprocessing.vectorization_ft(train_X['txt']) # 벡터화
        valid_X = preprocessing.vectorization_t(valid_X['txt']) # 벡터화


        print("=========================================================")
        print(train_X.shape)
        print(valid_X.shape)
        print("=========================================================")


        # Train!
        # xgbc = XGBClassifier(objective = 'multi:softprob', num_class = 2)
        xgbc = XGBClassifier()

        xgbc.fit(train_X, train_y)

        pred = xgbc.predict(valid_X)
        prob = xgbc.predict_proba(valid_X)

        # print('============================================================')
        # print(prob)
        # print('============================================================')

        f1 = f1_score(valid_y, pred)
        ac = accuracy_score(valid_y, pred) * 100

        if ac > best_ac:
            best_ac = ac

        if f1 > best_F1:
            best_F1 = f1
            best_model = xgbc
            pickle.dump(best_model, open('./model/best_f1_model(test).pkl', 'wb'))
            # preprocessing.best_vectorization(train_X['txt'])

        print(f'current f1 score : {f1}     best f1 score : {best_F1}')
        print(f'current accuracy : {ac}      best accuracy : {best_ac}')


train_X = preprocess(train_X)
print(train_X)
print(train_y)
train(train_X, train_y)