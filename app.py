# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import jieba
from nkubot import hello_lemon
import os
from aip import AipSpeech

APP_ID = '14891501'
API_KEY = 'EIm2iXtvDSplvR5cyHU8dAeM'
SECRET_KEY = '4KkGGzTq2GVrBEYPLXXWEEIoyLL1F6Zt '

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':  # 获取查询内容, 从request对象读取表单内容：
        if request.form.get('cont'):
            cont = request.form['cont']  # 内容
            return redirect(url_for('lemon', cont=cont))

    return render_template('lemon.html', rst=[('你好，我是小开～', '')])


@app.route('/lemon/<cont>', methods=['POST', 'GET'])
def lemon(cont):
    if request.method == 'POST':
        if request.form.get('cont'):  # 获取查询内容, 从request对象读取表单内容：
            cont = request.form['cont']
            return redirect(url_for('lemon', cont=cont))
    tmp, length = hello_lemon(cont)  # {0: [{},[]]}
    res = []
    for msg in tmp:
        res.append(msg)
    terms = list(jieba.cut_for_search(cont))
    rst = highlight(res, terms)
    if length != 0:
        os.system('mpg321 result.mp3')
        '''
        if re.match(r'(.*)(播放｜放｜想看)(.*)', cont):
            browser = webdriver.Chrome()
            # 最大化窗口
            browser.maximize_window()
            browser.get(res[0].get('link'))
            time.sleep(30)
            browser.close()
        '''
    os.system('mpg321 temp.mp3')
    return render_template('lemon.html', rst=rst, length=length)


def highlight(rs, tk):
    rst = []
    for pm in rs:
        title = pm.get('title')
        link = pm.get('link')
        # for t in tk:
        #     title = title.replace(t, '<em><font color="yellow">{}</font></em>'.format(t))
        rst.append((title, link))
    return rst


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
