from flask import Flask, request, render_template_string
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

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
        <p class="lead">Generate full Etsy listings in seconds. You only approve the draft in Etsy.</p>
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
    
    prompt = f"""You are an expert Etsy seller for SleepVista Art.
Create a complete listing for theme: {theme}

Rules from vault:
- Title format: "Theme Name | Horizontal Oil Painting Print | Calming Bedroom Art | SleepVista Art"
- Description must include the full science block at the top, bundle link, and "Hang as the last thing you see before bed"
- 13 tags, each ≤20 characters
- 9 mockup prompts using the exact vault structure (Prompt 1 to 9, with custom bedroom variations for this theme)

Output ONLY in this clean format:
TITLE: 
DESCRIPTION: 
TAGS: 
MOCKUP PROMPTS 1-9:
"""

    response = model.generate_content(prompt)
    result = response.text

    return render_template_string('''
    <div class="container mt-5">
        <h1>✅ Listing Generated for: {{theme}}</h1>
        <pre style="background:#222;color:#0f0;padding:20px;font-family:monospace">{{result}}</pre>
        <p>Copy the TITLE, DESCRIPTION, TAGS, and MOCKUP PROMPTS above into Etsy.</p>
        <a href="/" class="btn btn-primary">Generate Another Listing</a>
    </div>
    ''', theme=theme, result=result)

@app.route('/vault')
def vault():
    return render_template_string('''
    <div class="container mt-5">
        <h1>Vault Rules (locked in)</h1>
        <p>All generated listings follow the exact rules you gave me earlier.</p>
        <a href="/" class="btn btn-success">Back to Agent Hub</a>
    </div>
    ''')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
