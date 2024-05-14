from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan')

@app.route('/scan')
def scan():
    filepath = request.args.get('filepath')
    python_path = "python"  # Or your specific Python path if different
    command = [python_path, "meowlinter.py", "--html", filepath]

    # Execute the command and capture the output
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, error = process.communicate()

    # Decode the output and return it as HTML
    return output.decode('utf-8')

if __name__ == '__main__':
    app.run(debug=True)
