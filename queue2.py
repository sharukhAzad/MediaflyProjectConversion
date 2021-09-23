"""
AUTHOR

    Ron Yehoshua <ryehoshua@mediafly.com>    
"""

from flask import Flask, url_for, request
import queue
import json
from threading import Thread
import tempfile
import shutil

app = Flask(__name__)

num_threads = 1
dict_queues = {}

empty_queue_response = json.dumps({"result": "bad", "reason": "Nothing on the queue to pop"}, indent=2) + '\n'
no_such_queue_response = json.dumps({"result": "bad", "reason": "No such queue exists"}, indent=2) + '\n'
good_response = json.dumps({"result": "ok"}, indent=2) + '\n'
base_image_url = '/'

def reload_IMAGES():
    with open('images.json', 'r+') as fd:
        global IMAGES
        if fd:
            IMAGES = json.load(fd)
        else:
            IMAGES = {"images": []}

reload_IMAGES()

def add_to_queue(queuename, imagename):           
    reload_IMAGES()
    image_url = base_image_url + imagename
    json_event = {
                "id": imagename,
                "status": "pending",
                "original": image_url
            }
    counter = 0
    for image in IMAGES['images']:
        if image['id'] == imagename:
            image = json_event
            counter = -1
            break
        counter += 1
    if counter != -1:
        IMAGES['images'].append(json_event)
    f = open('oB3MYH6ANr', 'w')
    json.dump(IMAGES, f, indent=2)
    f.flush()
    f.close()
    shutil.move('oB3MYH6ANr', 'images.json')
    dict_queues[queuename].put(imagename)   

@app.route('/queues/<queuename>/push', methods=['POST'])
def push_to_queue(queuename):
    json_message = request.json            
    if queuename not in dict_queues:       
        dict_queues[queuename] = queue.Queue()              
    add_to_queue(queuename, json_message['id'])         
    return good_response, 200

@app.route('/queues/<queuename>/pop', methods=['POST'])
def pop_from_queue(queuename):
    try:
        reload_IMAGES()
        if queuename not in dict_queues:
            # return no_such_queue_response, 404
            dict_queues[queuename] = queue.Queue()
        imagename = dict_queues[queuename].get(timeout=5)
        return imagename, 200
    except:
        return empty_queue_response, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9090, debug=True, threaded=True, use_reloader=False)
    # app.run(host='0.0.0.0',port=9090, debug=True, processes=2)