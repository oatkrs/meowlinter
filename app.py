import subprocess
import os
from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask_cors import CORS
from flask_dropzone import Dropzone

app = Flask(__name__)
CORS(app)

app.config.update(
    DROPZONE_ALLOWED_FILE_CUSTOM=True,
    DROPZONE_ALLOWED_FILE_TYPE='.c,.cpp',
    DROPZONE_MAX_FILE_SIZE=3024,
    DROPZONE_MAX_FILES=1,
    DROPZONE_TIMEOUT=5*60*1000,
    DROPZONE_REDIRECT_VIEW='scanFile'
)

dropzone = Dropzone(app)

@app.route('/')
def index():
    return render_template('index.html',fileName='')

@app.route('/scan', methods=['POST'])
def scan():

    filename = request.form.get('fileName')
    code = request.form.get('code')

    filepath = os.path.join(os.path.dirname(__file__), filename)

    python_path = "python"

    error_log = []

    if code:
        try:
            with open(filepath, 'w') as f:
                f.write(code)
        except Exception as e:
            error_log.append(f"Error during file creation: {e}")

    try:
        meowlinter_path = os.path.join(os.path.dirname(__file__), 'meowlinter.py')
        command = [python_path, meowlinter_path, "--html", filepath,'>', 'output.csv']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, env=os.environ.copy())
        output, error = process.communicate()

        if error:
            error_log.append(f"Error during scan: {error}")

        result = output.decode('utf-8')

    except Exception as e:
        error_log.append(f"Error during scan: {e}")

    return render_template('result.html', result=result, error_log=error_log)

@app.route('/upload', methods=['POST'])
def upload():
    
    if request.method == 'POST':
        f = request.files.get('file')
        filepath = os.path.join(os.path.dirname(__file__), f.filename)
        f.save(filepath)
        global latestfile
        latestfile = f.filename
    return render_template('index.html',filename=f.filename)

@app.route('/scanFile')
def scanFile():
    filename = latestfile
    filepath = os.path.join(os.path.dirname(__file__), filename)

    python_path = "python"

    error_log = []

    try:
        meowlinter_path = os.path.join(os.path.dirname(__file__), 'meowlinter.py')
        command = [python_path, meowlinter_path, "--html", filepath,'>', 'output.csv']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, env=os.environ.copy())
        output, error = process.communicate()

        if error:
            error_log.append(f"Error during scan: {error}")

        result = output.decode('utf-8')

    except Exception as e:
        error_log.append(f"Error during scan: {e}")

    return render_template('result.html', result=result, error_log=error_log)





@app.route('/check_file')
def check_file():
    filename = request.args.get('filename')
    file_exists = os.path.exists(filename)
    return jsonify({'exists': file_exists})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=80)
