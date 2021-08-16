import numpy as np
from flask import Flask, request, jsonify, render_template
from cnn_predict import cnn_model

app = Flask(__name__) #Initialize the flask App
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('ec_text.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('ec_text.html', prediction_text='Current Description packsize is $ {}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)
