from flask import Flask, jsonify, request
#from flask_pymongo import PyMongo
#from bson.objectid import ObjectId
from flask_cors import CORS
from flair.models import TextClassifier
from flair.data import Sentence
from flask import session
import os, datetime
from werkzeug.utils import secure_filename
import uuid
from io import StringIO
import csv

app = Flask(__name__)
app.secret_key = "super_secret_key"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # app.config['SECRET_KEY'] = 'oh_so_secret'

# app.config['MONGO_DBNAME'] = 'exposeModel'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/exposeModel'
# mongo = PyMongo(app)

CORS(app)
classifier = TextClassifier.load('models/best-model2.pt')

@app.route('/', methods=['GET'])
def index():
    return jsonify("welcome to Arafa API")

@app.route('/api/tasks', methods=['GET'])
def get_result():
    result = []
    try:
        result = session['my_result']
    except:
        result = result
    return jsonify(result)

@app.route('/api/task', methods=['POST'])
def input_predict_text():
    file = request.files['file']
    result = []
    
    
    if file.filename:
        filename = secure_filename(file.filename)

        # Gen GUUID File Name
        fileExt = filename.split('.')[1]
        autoGenFileName = uuid.uuid4()

        newFileName = str(autoGenFileName) + '.' + fileExt

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], newFileName)    )
        
        
        with open(os.path.join(app.config['UPLOAD_FOLDER'], newFileName), "r") as f:
            if fileExt == 'txt':
                content = f.readlines()
            elif fileExt == 'csv':
                content = csv.reader(f, delimiter=' ')  
            result = predict(content, fileExt)
              


    session['my_result'] = result
    return jsonify(result)

def predict(content, fileExt):
    result = []
    id = 0
    for line in content:
        # sentences.append(Sentence(line))
        if fileExt == 'csv':
            line = ' '.join(map(str, line))
        sentence = Sentence(line)
        classifier.predict(sentence)
        text = sentence.to_plain_string()
        # textLines.append(text)
        label = sentence.labels[0]
        # labels.append(label.value)
        id = id+1
        prediction = {'ID': id, 'title': text, 'tag': label.value}
        result.append(prediction)
    return result

if __name__ == '__main__':
    app.run(debug=True)
