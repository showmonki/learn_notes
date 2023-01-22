# coding=utf8
import io
import json
import os
from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request,render_template

file_path = os.path.dirname(__file__)
app = Flask(__name__)
imagenet_class_index = json.load(open(os.path.join(file_path,'imagenet_class_index.json')))
model = models.densenet121(pretrained=True)
model.eval()


def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        class_id, class_name = get_prediction(image_bytes=img_bytes)
        print(class_name)
        data = {}
        data['status'] = 'SUCCESS'
        data['result'] = {'class_id': class_id, 'class_name': class_name}
        return jsonify(data)


@app.route('/ajax_form', methods=['POST'])
def ajax_form():
    if request.method == 'POST':
        data = {}
        data['status'] = 'SUCCESS'
        data['log_info'] = request.form['username']
        return jsonify(data)


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        img = Image.open(file.stream)
        print(img)
        return img


@app.route('/', methods=['GET','POST'])
def index():
    return render_template("test1.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
