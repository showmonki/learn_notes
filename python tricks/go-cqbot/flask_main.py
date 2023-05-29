import requests
from flask import Flask, request
app=Flask(__name__)
@app.route('/', methods=["POST"])
def QQBot():
    p='0'
    if request.get_json().get('message_type')=='private':
        qq_id = request.get_json().get('sender').get('user_id')
        nickname=request.get_json().get('sender').get('nickname')
        message=request.get_json().get('message')
        print(qq_id, nickname, message)
        resq=requests.get('http://127.0.0.1:5700/send_private_msg?user_id={0}&message={1}'.format(qq_id, message))
        print(resq)
        print('http://127.0.0.1:5700/send_private_msg?user_id={0}&message={1}'.format(qq_id, message))
    print(request.get_json())
    return p

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5709)
