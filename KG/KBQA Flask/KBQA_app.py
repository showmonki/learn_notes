import numpy as np
from flask import Flask, request, jsonify, render_template
from KBQA.kbqa_main import KBQAChat

app = Flask(__name__) #Initialize the flask App


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_answer',methods=['POST'])
def get_answer():
    '''
    For rendering results on HTML GUI
    '''
    Question = request.form.get('Question')
    kbqa_service = KBQAChat()
    output = kbqa_service.get_answer(Question)
    return render_template('index.html', Answer_text='回复: %s' % output)


if __name__ == "__main__":
    app.run(debug=True)
