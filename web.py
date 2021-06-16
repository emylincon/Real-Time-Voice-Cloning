from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from datetime import timedelta
import codecs as c
import time
from werkzeug.utils import secure_filename
from VoiceClone import Demo
import json
import numpy as np

app = Flask(__name__)
app.secret_key = "28wrifn43qwrpfo24wrefichl"
app.permanent_session_lifetime = timedelta(minutes=60)
CLONE_OBJ = Demo.Clone(location='root')


@app.route('/home')
def home():
    return redirect('/')


@app.route('/')
def index():
    session.permanent = True
    session['user'] = 'emeka'
    return render_template('index.html')


@app.route('/capture')
def capture():
    return render_template('capture.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


def fin2(base_string, file_name):  # this writes the image to disk
    str_obj = base_string.split('base64')[1][1:].encode()
    fh = open(file_name, "wb")
    fh.write(c.decode(obj=str_obj, encoding='base64'))
    fh.close()


@app.route('/cloning')
def cloning():
    if session.get('embed') is not None:
        return render_template('results.html')
    else:
        # return render_template('results.html')
        return redirect(url_for('home'))


@app.route('/clone_api', methods=['POST'])
def clone_api():
    try:
        json_req = request.get_json()
        audio = CLONE_OBJ.clone_voice(np.array(session['embed']), json_req['message'])
        return jsonify({'result': audio}), 201
    except Exception as e:
        return jsonify({'error': f'{e}'}), 404


@app.route('/okay', methods=['POST', 'GET'])
def okay():
    if request.method == 'POST':
        json_req = request.get_json()
        return jsonify({'result': session['user'], 'data': json_req})
    else:
        return jsonify({'result': session['user']})


def process_audio(audio_file):
    full_name = f'VoiceClone/audio/{round(time.time())}.weba'
    audio_file.save(full_name)
    embed = CLONE_OBJ.process_voice(full_name)
    return embed.tolist()


@app.route('/audioUpload', methods=['POST'])
def audio():
    sent_file = request.files['audio-file']
    session['embed'] = process_audio(sent_file)

    # print(embed == np.array(session['embed']))
    return jsonify({'result': 'done'})


@app.route('/process', methods=['POST', 'GET'])
def process():
    if request.method == 'POST':

        sent_file = request.files['file']
        session['embed'] = process_audio(sent_file)

        return redirect(url_for('cloning'))
    else:
        return home()


if __name__ == '__main__':
    app.run(debug=True)