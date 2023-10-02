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
import json
from flaskext.mysql import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '3048'
app.config['MYSQL_DATABASE_DB'] = 'board'

mysql.init_app(app)

cursor = mysql.connect().cursor()

# 메인 화면
@app.route("/")
def main():
    return render_template('index.html')

# 인공지능 결과 보기
@app.route("/result", methods=['POST'])
def send_text():
    data = request.get_json()
    content = data['content']


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
        return percentage
    
    # text = request.form.get('text')
    result = sentiment_predict(content)
    if(result >= 75):
        # print("{:.2f}% 확률로 보이스피싱입니다.\n".format(score * 100))
        # print("*경고* 보이스 피싱 입니다. 즉시 경찰서에 연락하거나 전화를 끊으십시오.")
        result="{:.2f}".format(result)
        return jsonify({"result": result})
    elif(result >= 50):
        # print("{:.2f}% 확률로 보이스피싱입니다.\n".format(score * 100))
        # print("*주의* 보이스피싱 위험 단계 입니다. 보이스피싱 같다면 전화를 끊으십시오.")
        # return render_template('return2-mid.html',result = "{:.2f}".format(result))
        result="{:.2f}".format(result)
        return jsonify({"result": result})
    elif(result >= 25):
        # print("{:.2f}% 확률로 보이스피싱입니다.\n".format(score * 100))
        # print("보이스 피싱 의심 단계 입니다.")
        # return render_template('return3-ok.html',result = "{:.2f}".format(result))
        result="{:.2f}".format(result)
        return jsonify({"result": result})
    else:
        # print("{:.2f}% 확률로 보이스피싱입니다.\n".format(score * 100))
        # print("보이스 피싱 안전 단계 입니다.")
        # return render_template('return3-ok.html',result = "{:.2f}".format(result))
        result="{:.2f}".format(result)
        return jsonify({"result": result})
    

#게시판 조회
@app.route('/board',methods=['GET'])
def board():
    cursor.execute("select name, title from board.board")

    res = []
    col = tuple([d[0] for d in cursor.description])


    for row in cursor:
        res.append(dict(zip(col, row)))

    print(res)
    return json.dumps(res)

# 글 쓰기 화면
@app.route('/board/write', methods=["GET"])
def write():
    return render_template("write.html")

# 글 게시하기
@app.route('/board/post', methods=["POST"])
def posting():
    data = request.get_json()

    name = data['name']
    title = data['title']
    content = data['content']

    sql = "INSERT INTO board.board (name, title, content) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, title, content))
    cursor.connection.commit()

    return jsonify({"message": "글이 정상적으로 등록되었습니다."}), 201

#글 보기
@app.route('/board/<id>', methods=["GET"])
def watch(id):
    sql = "select name, title, content from board.board where id = %s"
    cursor.execute(sql,(id,))  
    
    col = [x[0] for x in cursor.description]

    for row in cursor:
        res = dict(zip(col, row))

    print(res)
    return json.dumps(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
