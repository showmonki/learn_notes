# coding = utf-8
from flask import Flask, request, jsonify, render_template

app = Flask(__name__) #Initialize the flask App


def split_str(input_str):
    input_list = input_str.split('-')
    return input_list


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/result',methods=['POST'])
def main_func():
    # int_features = [int(x) for x in request.form.values()]
    output = request.form['name']
    return render_template('index.html', result_text='Current name:{}'.format(output))


@app.route('/date',methods=['GET'])
def split_date():
    input_str = request.args.get('date')
    return jsonify({'status': 200, 'message': 'success', 'result': split_str(input_str)})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)  # host='0.0.0.0'
