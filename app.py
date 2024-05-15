import subprocess
import os
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from flask_dropzone import Dropzone

app = Flask(__name__)
CORS(app)

app.config.update(
    DROPZONE_ALLOWED_FILE_CUSTOM=True,
    DROPZONE_ALLOWED_FILE_TYPE='.c,.cpp',
    DROPZONE_MAX_FILE_SIZE=3024,
    DROPZONE_MAX_FILES=1,
    DROPZONE_IN_FORM=True,
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_UPLOAD_ACTION='scan',
    DROPZONE_TIMEOUT=5*60*1000
)

dropzone = Dropzone(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():

    print(request.form)

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
        command = [python_path, meowlinter_path, "--html", filepath]
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
