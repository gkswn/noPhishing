from flask import Flask, request, render_template, jsonify
import numpy as np
import pandas as pd
import tensorflow as tf
import preprocessing
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
import re
import pickle

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')


@app.route("/receive", methods=['POST'])
def send_text():
    loaded_model = load_model('best_model.h5')
    max_len = 1000
    stopword = preprocessing.make_stopword()

    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    
    def sentiment_predict(new_sentence):
        # 정규식을 사용하여 문자열 처리
        new_sentence = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", new_sentence)
        new_sentence = re.sub('^ +', '', new_sentence)
        new_sentence = preprocessing.tokenize(new_sentence) # 토큰화
        new_sentence = preprocessing.del_stopword(new_sentence, stopword) # 불용어 제거
        stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다'] # 추가 불용어
        new_sentence = preprocessing.del_stopword(new_sentence, stopwords) # 추가 불용어 제거
        encoded = tokenizer.texts_to_sequences([new_sentence]) # 정수 인코딩
        pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
        score = float(loaded_model.predict(pad_new)[0]) # 예측
        percentage = score*100 # 보이스 피싱 확률 계산
        return percentage,score
    
    text = request.form.get('text')
    result,score = sentiment_predict(text)
    if(result >= 75):
        print("{:.2f}% 확률로 보이스피싱입니다.\n".format(score * 100))
        print("*경고* 보이스 피싱 입니다. 즉시 경찰서에 연락하거나 전화를 끊으십시오.")
        return render_template('return1-danger.html',result="{:.2f}".format(result))
    elif(result >= 50):
        print("{:.2f}% 확률로 보이스피싱입니다.\n".format(score * 100))
        print("*주의* 보이스피싱 위험 단계 입니다. 보이스피싱 같다면 전화를 끊으십시오.")
        return render_template('return2-mid.html',result = "{:.2f}".format(result))
    elif(result >= 25):
        print("{:.2f}% 확률로 보이스피싱입니다.\n".format(score * 100))
        print("보이스 피싱 의심 단계 입니다.")
        return render_template('return3-ok.html',result = "{:.2f}".format(result))
    else:
        print("{:.2f}% 확률로 보이스피싱입니다.\n".format(score * 100))
        print("보이스 피싱 안전 단계 입니다.")
        return render_template('return3-ok.html',result = "{:.2f}".format(result))
    

@app.route("/result", methods=['POST'])
def result():
    text = request.form.get('text')
    if float(text) >= 75:
        return render_template('return1-danger.html', text=text)
    elif float(text) >= 50:
        return render_template('return2-middle.html', text=text)
    else:
        return render_template('return3-ok.html', text=text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    