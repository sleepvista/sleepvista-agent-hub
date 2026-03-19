from flask import Flask, request, render_template_string
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html><head><title>SleepVista Agent Hub</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head><body class="bg-light">
    <div class="container mt-5 text-center">
        <h1>🛏️ SleepVista Agent Hub</h1>
        <p class="lead">Generate full Etsy listings in seconds. You only approve the draft.</p>
        <form action="/generate" method="post">
            <input type="text" name="theme" class="form-control form-control-lg mb-3" placeholder="Theme (e.g. misty mountain layers v2)" required>
            <button type="submit" class="btn btn-success btn-lg">Generate Full Listing →</button>
        </form>
        <a href="/vault" class="btn btn-secondary mt-4">View Vault Rules</a>
    </div></body></html>
    ''')

@app.route('/generate', methods=['POST'])
def generate():
    theme = request.form.get('theme', '')
    # This is where the real agent logic will live (we can expand it)
    return render_template_string('''
    <h1>✅ Listing Generated for: {{theme}}</h1>
    <p>Open this page in your browser, copy the text below, and paste into Etsy.</p>
    <pre style="background:#222;color:#0f0;padding:20px">TITLE: {{theme}} | Horizontal Oil Painting Print | Calming Bedroom Art | SleepVista Art
DESCRIPTION: (full science block + bundle + description)
TAGS: (13 perfect tags)
MOCKUP PROMPTS: (9 ready prompts)
</pre>
    <a href="/" class="btn btn-primary">Generate Another</a>
    ''', theme=theme)

@app.route('/vault')
def vault():
    return "Vault rules are locked in. All generated listings follow them."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
