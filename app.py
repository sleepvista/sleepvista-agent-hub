from flask import Flask, request, render_template_string

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
        <p class="lead">Your marketplace is now live and stable!</p>
        <form action="/generate" method="post">
            <input type="text" name="theme" class="form-control form-control-lg mb-3" placeholder="Type a theme (e.g. misty mountain layers v2)" required>
            <button type="submit" class="btn btn-success btn-lg">Generate Listing</button>
        </form>
    </div></body></html>
    ''')

@app.route('/generate', methods=['POST'])
def generate():
    theme = request.form.get('theme', 'test')
    return f'''
    <div class="container mt-5">
        <h1>✅ Generated for: {theme}</h1>
        <p>This is the stable base version. Next step: full Gemini-powered listings.</p>
        <a href="/" class="btn btn-primary">Back to Home</a>
    </div>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
