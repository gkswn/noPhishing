import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from konlpy.tag import Mecab

import pickle

# 결측치 제거
def drop_na(df):
    df.dropna(inplace=True)
    
    return df

# 특수기호 제거
def del_specific(df):

    df['txt'] = df['txt'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","", regex=True) # 정규 표현식 수행.
        
    return df

# 불용어 제거
def del_stopword(document, stopword):

    return [document[i] for i in range(len(document)) if not document[i] in stopword]

# 문장 토큰화
def tokenize(document):
    
    mecab = Mecab(dicpath=r"C:\mecab\mecab-ko-dic")
    result = mecab.morphs(document)

    return result

# 벡터화 (적합 및 변환)
def vectorization_ft(df):
    
    # 리스트 형식 문자열로 바꿔줌
    df = df.apply(lambda x : ' '.join(x)) 
    
    # fit_transform을 이용하여 학습과 변환을 한 번에 진행
    tfvec = TfidfVectorizer()
    result = tfvec.fit_transform(df)
    
    # Save pickle (객체로 저장)
    with open('./encoder/tfidfv.pickle', 'wb') as fw:
        pickle.dump(tfvec, fw)
    
    return result

# 벡터화 (단순변환)
def vectorization_t(df):
    
    # 리스트 형식 문자열로 바꿔줌
    df = df.apply(lambda x : ' '.join(x)) 
    
    # Vectorizer 불러오기
    with open("./encoder/tfidfv.pickle","rb") as fr:
        tfvec = pickle.load(fr)
    
    # Transform
    result = tfvec.transform(df)
    
    return result

# best vectorization 저장. ( 이거 동작이 안댐 )
def best_vectorization(df):

    df = df.apply(lambda x : ' '.join(x))

    tfvec = TfidfVectorizer()
    out = tfvec.fit_transform(df)

    # tfvec = encoder
    with open('./encoder/best_vectorization.pkl', 'wb') as fw:
        pickle.dump(tfvec, fw)

    return out

# 불용어 리스트 제작
def make_stopword():
    t_file_name = open('./data/stopword.txt','r',encoding='utf-8')

    stopword = []

    for line in t_file_name.readlines():
        stopword.append(line[:-1])
        
    stopword = list(set(stopword))
    
    return stopword

