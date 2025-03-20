import sys
import io
from flask import Flask, render_template_string
import predictor

app = Flask(__name__)

@app.route('/')
def index():
    sys.stdout = io.StringIO()  # capture terminal output
    predictor.main()  # use the module name directly
    output = sys.stdout.getvalue()
    sys.stdout = sys.__stdout__  # reset stdout

    return render_template_string("""
    <html>
        <head><title>Basketball AI Output</title></head>
        <body>
            <h1>Basketball AI Predictions</h1>
            <pre>{{ output }}</pre>
        </body>
    </html>
    """, output=output)

if __name__ == "__main__":
    app.run(debug=True)
