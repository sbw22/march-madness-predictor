from flask import Flask, Response
import time
import subprocess

app = Flask(__name__)

# generator function to stream terminal output
def generate_output():
    # process output from predictor
    process = subprocess.Popen(['python3', 'predictor.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    
    # read and yield output line by line
    for line in iter(process.stdout.readline, b''):
        yield line.decode('utf-8') + '<br>'
    
    # capture any errors
    for line in iter(process.stderr.readline, b''):
        yield f'<b>Error:</b> {line.decode("utf-8")}<br>'

@app.route('/') # boot flask
def index():
    return Response(generate_output(), mimetype='text/html') # use mimetext to convert to HTML
# run main function from predictor
if __name__ == '__main__':
    app.run(debug=True)
