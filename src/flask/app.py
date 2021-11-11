from flask import Flask, jsonify
#from flask_cors import CORS
from compressImage import compressImage
import json
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
#CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET','POST'])
def ping_pong():
    f = open('D:/Tugas Andre/ITB/IF/Semester 3/Aljabar Linear dan Geometri/Tubes 2/Algeo02-20039/src/vue/Data/image.json')
    data = json.load(f)
    base = data["image"][0]['base64']
    print(base)
    percentage = 80 
    compressImage(base,percentage)


if __name__ == '__main__':
    ping_pong()