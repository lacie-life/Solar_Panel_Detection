from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
import os
import glob
import sys
import binascii
import argparse

import time

app = Flask("Solar Panel Detection")
app.config['IMAGE_EXTS'] = [".png", ".jpg", ".jpeg", ".gif", ".tiff", ".JPG"]


def encode(x):
    print(x)
    print(binascii.hexlify(x.encode('utf-8')).decode())
    return binascii.hexlify(x.encode('utf-8')).decode()


def decode(x):
    return binascii.unhexlify(x.encode('utf-8')).decode()


@app.route('/')
def home():
    root_dir = app.config['ROOT_DIR']
    result_dir = app.config['RESULT_DIR']
    image_paths = []
    result_paths = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in app.config['IMAGE_EXTS']):
                image_paths.append(encode(os.path.join(root, file)))

#    for result, dirs, files in os.walk(result_dir):
#        for file in files:
#            if any(file.endswith(ext) for ext in app.config['IMAGE_EXTS']):
#               result_paths.append(encode(os.path.join(result, file)))
    return render_template('index.html', paths=image_paths, result_paths=result_paths)


@app.route('/cdn/<path:filepath>')
def download_file(filepath):
    dir, filename = os.path.split(decode(filepath))
    return send_from_directory(dir, filename, as_attachment=False)


@app.route('/results/<path:filepath>')
def upload_file(filepath):
    dir, filename = os.path.split(decode(filepath))
    # time.sleep(1)
    dir = "assets/results"
    return send_from_directory(dir, filename, as_attachment=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Usage: %prog [options]')
    parser.add_argument('-path', help='Gallery root directory path', default='assets/images')
    parser.add_argument('-result_path', help='Gallery result directory path', default='assets/results')
    parser.add_argument('-l', '--listen', dest='host', default='192.168.0.244', \
                        help='address to listen on [127.0.0.1]')
    parser.add_argument('-p', '--port', metavar='PORT', dest='port', type=int, \
                        default=18000, help='port to listen on [5000]')
    args = parser.parse_args()
    app.config['ROOT_DIR'] = args.path
    app.config['RESULT_DIR'] = args.result_path
    app.run(host=args.host, port=args.port, debug=False)
