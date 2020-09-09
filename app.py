import flask
from flask import request, jsonify, render_template, url_for, abort
import requests
import json
import water_level_anomalous
import numpy as np
import random
import os
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api
import requests


app = flask.Flask(__name__)
api = Api(app)


app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Water Level Detection</h1>
<p>A prototype API for detect the abnormal wave.</p>'''


# Get the data from the api created from Laravel, and then  
@app.route('/api/getdata', methods=['GET'])
def api_all():
    r = requests.get('https://richard2020.djtechtw.com/api/waterlevel/index')
    data = r.json()
    # anomalous_indexes = water_level_anomous.draw_graph(in_array)
    # print(in_array)
    # records2 ={"items" : sorted(records["item"], key=lambda d: d["id"])}

    # sort id
    # data = sorted(data, key=lambda k: data[k]['id'], reverse=True)
    # print(data)

    # Getting the data
    in_array = []
    for i in range(len(data)):

        in_array.append(float(data[i]['water_level']))

    # Pass the data into the module for detecting anomalous values
    anomalous_indexes = water_level_anomalous.draw_graph(in_array=in_array)

    # Put tags on thoese anomalous ones
    # put_tags(anomalous_indexes)

    # Pass the generated image to the api for sending Line message
    push_image()
    return(r.text)


@app.route('/api/putTags', methods=['PUT'])
def put_tags(anomalous_indexes):
    id = str(anomalous_indexes[0] + 1)

    r = requests.put('https://richard2020.djtechtw.com/api/waterlevel/' + id + '/update', data = {'tags':'*'})
    return '''<h1>Tags have been updated</h1>'''

# Generating random samples for testing
@app.route('/api/postSamples', methods=['GET','POST'])
def post_samples():

    for i in range(0, 300):
        random_level = random.randint(280, 330)
        water_level = float(random_level)
        if(i == 40):
            water_level = 100.2


        r = requests.post('https://richard2020.djtechtw.com/api/waterlevel/store', data = {'water_level':water_level, 'uuid':'a6784272-aca9-4a82-9267-c9b1ba3a9cb9'})
    return '''<h1>Tags have been updated</h1>'''

@app.route('/api/postImage', methods=['GET', 'POST'])
def push_image():
 
    image_url = 'plot.png'

    url = "https://richard2020.djtechtw.com/api/waterdetection/image"

    payload = {}
    files = [
    ('image', open(image_url,'rb'))
    ]
    headers= {}

    response = requests.request("POST", url, headers=headers, data = payload, files = files)

    print(response.text.encode('utf8'))

    return '''<h1>Image uploaded</h1>'''

if __name__ == "__main__":

    app.run()
