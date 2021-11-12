from flask import Flask, jsonify,send_file
from flask_cors import CORS
from compressImage import compressImage
import json
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET','POST'])
def ping_pong():
    f = open('D:/Tugas Andre/ITB/IF/Semester 3/Aljabar Linear dan Geometri/Tubes 2/Algeo02-20039/src/vue/Data/image.json')
    data1 = json.load(f)
    base = data1["image"][0]['base64']
    percentage = data1["image"][0]['percentage'] 
    base2 = base.split(',', 1)[1]
    compressImage(base2,percentage)    
    return send_file('../vue/src/assets/test.jpg') #jsonify('abc') 

if __name__ == '__main__':
    app.run()