from flask import Flask, render_template, url_for, request, session, redirect, jsonify
from datetime import timedelta
import codecs as c
import time
import wget
from werkzeug.utils import secure_filename
from VoiceClone import Demo

app = Flask(__name__)
app.secret_key = "28wrifn43qwrpfo24wrefichl"
app.permanent_session_lifetime = timedelta(minutes=60)
output = 1
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


@app.route('/process/<path:url>')
def process(url):
    audio_path = f'VoiceClone/audio/{output:03}.weba'
    wget.download(url, audio_path)
    embed = CLONE_OBJ.process_voice(audio_path)
    session['embed'] = embed
    redirect(url_for('cloning'))


@app.route('/cloning')
def cloning():
    if session.get('embed') is not None:
        return render_template('results.html')
    else:
        return render_template('results.html')
        # return redirect(url_for('home'))


@app.route('/clone_api', methods=['POST'])
def clone_api():
    try:
        json_req = request.get_json()
        audio = CLONE_OBJ.clone_voice(session['embed'], json_req['message'])
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

@app.route('/compare', methods=['POST', 'GET'])
def compare():
    if request.method == 'POST':

        sent_file = request.files['file']
        full_name = f"{int(time.time())}" + secure_filename(sent_file.filename)
        f_name = f'static/temp/{full_name}'
        sent_file.save(f_name)
        result = None

        return render_template('results.html', res=result)
    else:
        return home()


if __name__ == '__main__':
    app.run(debug=True)