#!/usr/bin/env python
"""
AUTHOR

    Ron Yehoshua <ryehoshua@mediafly.com>
"""

import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import json
from threading import Thread
import requests

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './'

IMAGES = None
fd = None
not_found_response = json.dumps({"result": "ok", "reason": "Image not found"}, indent=2) + '\n'
empty_queue_response = json.dumps({"result": "bad", "reason": "Nothing on the queue to pop"}, indent=2) + '\n'
good_response = json.dumps({"result": "ok"}, indent=2) + '\n'

def reload_IMAGES():
    with open('images.json', 'r+') as fd:
        global IMAGES
        if fd:
            IMAGES = json.load(fd)
        else:
            IMAGES = {"images": []}

reload_IMAGES()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        print 'file: ' + str(file)
        if file:
            filename = secure_filename(file.filename)
            print 'filename: ' + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            url = 'http://localhost:9090/queues/jobs/push'
            data = {"id": filename}
            headers = {"Content-type": "application/json", 'Accept': 'text/plain'}
            r = requests.post(url, data=json.dumps(data), headers=headers)
        return redirect(url_for('index'))
    reload_IMAGES()
    return render_template('index.html', images=IMAGES)

@app.route('/<filename>')
def uploaded_file(filename):
    reload_IMAGES()
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/images')
def get_all_images():
    reload_IMAGES()
    return json.dumps(IMAGES['images'], indent=2) + '\n'

@app.route('/images/<imagename>', methods=['GET', 'PUT'])
def image(imagename):
    reload_IMAGES()
    if request.method == 'PUT':
        filename = secure_filename(imagename)
        url = 'http://localhost:9090/queues/jobs/push'
        data = {"id": filename}
        headers = {"Content-type": "application/json", 'Accept': 'text/plain'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        return good_response
    else:
        for image in IMAGES['images']:
            if image['id'] == imagename:
                return json.dumps(image, indent=2) + '\n'
        return not_found_response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
