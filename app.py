import subprocess
import os
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    filepath = request.form.get('filepath')
    code = request.form.get('code')
    python_path = "python"

    if code:
        try:
            with open(filepath, 'w') as f:
                f.write(code)
        except Exception as e:
            return f"Error saving code to file: {e}"

    try:
        meowlinter_path = os.path.join(os.path.dirname(__file__), 'meowlinter.py')
        command = [python_path, meowlinter_path, "--html", filepath]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, env=os.environ.copy())
        output, error = process.communicate()

        if error:
            return f"Error during scan: {error.decode('utf-8')}"

        return output.decode('utf-8')

    except Exception as e:
        return f"Error during scan: {e}"

@app.route('/check_file')
def check_file():
    filename = request.args.get('filename')
    file_exists = os.path.exists(filename)
    return jsonify({'exists': file_exists})

if __name__ == '__main__':
    app.run(debug=True)
