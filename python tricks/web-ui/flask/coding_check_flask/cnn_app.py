import numpy as np
from flask import Flask, request, jsonify, render_template
from cnn_predict import CnnModel
from cnn_function import load_category

app = Flask(__name__) #Initialize the flask App

@app.route('/')
def home():
    return render_template('ec_text.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    seg,desc,num_top_item  = request.form.values()
    save_name_sub = 'character_cnn'  # train的语句里时候有这个文件结构。以防文件乱掉。暂时不改动这句
    train_dir = 'Model/input/{}/'.format(seg)
    save_path = 'Model/checkpoints/{}/{}/best_validation'.format(seg, save_name_sub)
    vocab_dir = 'Model/output/{}/{}/vocab.txt'.format(seg, save_name_sub)
    categories, cat_to_id = load_category(train_dir)
    num_classes = len(cat_to_id)
    cnn_model = CnnModel(num_classes,train_dir,vocab_dir,save_path)
    output = cnn_model.predict(desc,int(num_top_item))
    return render_template('ec_text.html', CNN_result='Current Description is {}\n Requested Seg is {}\n Prediction is {}'.format(desc,seg,output))


if __name__ == "__main__":
    app.run(debug=True)
