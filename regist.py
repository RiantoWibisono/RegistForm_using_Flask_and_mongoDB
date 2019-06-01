from flask import Flask, render_template, jsonify, request, send_from_directory
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = './storage'
x = MongoClient('mongodb://localhost:27017/')
db = x['testdb']
col = db['employee']

@app.route('/')
def home():
    return render_template('mainform.html')

@app.route('/data', methods = ['GET', 'POST'])
def data():
    if request.method == 'GET':
        jml = col.find().count()
        if jml > 0:
            dataJson = []
            for i in col.find():
                id = i['_id']
                name = i['name']
                age = i['age']
                link = i['link']
                dataDict = {
                    "_id": str(id),
                    "name": name,
                    "age": age,
                    "link": link
                }
                dataJson.append(dataDict)
            return jsonify(dataJson)
        else:
            return jsonify({'status': 'No data available'})
    else:
        name = request.form['name']
        age = request.form['age']
        data = request.files['photo']

        namefile = secure_filename(data.filename)                       
        data.save(os.path.join(app.config['UPLOAD_FOLDER'], namefile))  
        link = 'http://127.0.0.1:5000/upload/' + namefile

        dataDict = {
            "name": name,
            "age": age,
            "link": link
        }
        col.insert_one(dataDict)
        return render_template('successpage.html', name = name, age = age, link = link)

@app.route('/upload/<namefile>')
def upload(namefile):
    return send_from_directory('./storage', namefile)

if __name__ == '__main__':
    app.run(debug = True)