#!/usr/bin/env python3
import argparse
import pathlib
import subprocess

from shutil import copyfile

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask_cors import CORS

from util import m2_to_json


def annotate(orig, cor):
    pathlib.Path('tmp').mkdir(exist_ok=True)

    with open('tmp/orig', 'w') as fp:
        for sent in orig:
            fp.write(sent.strip() + '\n')

    with open('tmp/cor', 'w') as fp:
        for sent in cor:
            fp.write(sent.strip() + '\n')

    p = subprocess.Popen(
        'python3 ../parallel_to_m2.py -orig tmp/orig -cor tmp/cor -out tmp/out',
        shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()

    with open('tmp/out') as fp:
        annotations = fp.read().split('\n')

    copyfile('tmp/out', args.sentences + '.aann')
    annotations_json = m2_to_json(args.sentences + '.aann')

    return annotations, annotations_json

def create_app(config=None):
    app = Flask(__name__, static_url_path='/static', template_folder='template')

    # See http://flask.pocoo.org/docs/latest/config/
    app.config.update(dict(DEBUG=True))
    app.config.update(config or {})

    CORS(app)

    @app.route('/')
    def root():
        return render_template('index.html')

    @app.route('/load')
    def data():
        return jsonify(orig)


    @app.route('/save', methods=['POST'])
    def save():
        data = request.json
        cor = data
        annotations, annotations_json = annotate(orig, cor)
        return jsonify({'raw': annotations, 'json': annotations_json})

    return app


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', action='store', default='8000')
    parser.add_argument('sentences', type=str, help='path to a list of tokenized sentences, one per line')

    args = parser.parse_args()

    with open(args.sentences) as fp:
        orig = fp.readlines()

    port = int(args.port)
    app = create_app()
    app.run(host='0.0.0.0', port=port)
