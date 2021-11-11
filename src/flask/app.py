from flask import Flask, jsonify
from flask_cors import CORS
from compressImage import compressImage
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET','POST'])
def ping_pong(base,percentage):
    return  compressImage(base,percentage)


if __name__ == '__main__':
    app.run()