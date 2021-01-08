import requests
from time import sleep
from imageprocessing import process_image
import json
import sys
import tempfile
import shutil

IMAGES = None
base_image_url = '/'

def reload_IMAGES():
    with open('images.json', 'r+') as fd:
        global IMAGES
        if fd:
            IMAGES = json.load(fd)
        else:
            IMAGES = {"images": []}

reload_IMAGES()


def do_work(url, queuename):
    while True:
        sys.stdout.write("Popping queue '{}'...".format(queuename))
        sys.stdout.flush()
        r = requests.post('http://localhost:9090' + '/queues/' + queuename + '/pop')
        if r.status_code != requests.codes.ok:
            try:
                print ' ({}) reason: {}'.format(r.status_code, r.json()['reason'])
            except:
                print ' ({})\n{}'.format(r.status_code, r.text)
        else:
            reload_IMAGES()
            imagename = r.content
            print '  found imagename: ' + str(imagename)
            processed_filename = process_image(imagename)
            json_event = {"id": imagename, "original": base_image_url + imagename}
            if processed_filename:
                json_event['status'] = "completed"
                json_event['processed'] = base_image_url + processed_filename
            else:
                json_event['status'] = "failed"
            counter = 0
            for image in IMAGES['images']:
                if image['id'] == imagename:
                    IMAGES['images'][counter] = json_event
                    break
                counter += 1
            f = open('oB3MYH6ANr', 'wb')
            json.dump(IMAGES, f, indent=2)
            f.flush()
            f.close()
            shutil.move('oB3MYH6ANr', 'images.json')


if __name__ == '__main__':
    counter = 1
    num_args = len(sys.argv)
    url = "http://127.0.0.1:8080"
    queuename = "jobs"
    help_statement = ('usage: python ContentServerEncryption.py -u, -q'
                     '\n -u <url>, -q <queuename>')
    while counter < num_args:
        if sys.argv[counter] == '-h':
            print help_statement
            sys.exit(2)
        elif sys.argv[counter] == '-u':
            url = sys.argv[counter + 1]
        elif sys.argv[counter] == '-q':
            queuename = sys.argv[counter + 1]
        counter += 2

    do_work(url, queuename)
