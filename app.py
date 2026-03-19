from flask import Flask, request, render_template_string
import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html><head><title>SleepVista Agent Hub</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>body{background:#f8f9fa}</style>
    </head><body>
    <div class="container mt-5 text-center">
        <h1>🛏️ SleepVista Agent Hub</h1>
        <p class="lead">Generate full Etsy listings in seconds.<br>You only approve the draft in Etsy.</p>
        <form action="/generate" method="post" class="mt-4">
            <input type="text" name="theme" class="form-control form-control-lg" placeholder="Theme (e.g. misty mountain layers v2)" required>
            <button type="submit" class="btn btn-success btn-lg mt-3">Generate Full Listing →</button>
        </form>
    </div></body></html>
    ''')

@app.route('/generate', methods=['POST'])
def generate():
    theme = request.form.get('theme', '')
    
    prompt = f"""You are an expert Etsy seller for SleepVista Art.
Create a complete listing for theme: {theme}

Rules from vault (follow exactly):
- Title format: "Theme Name | Horizontal Oil Painting Print | Calming Bedroom Art | SleepVista Art"
- Description: Start with bundle link, then full science block, then description, end with "Hang as the last thing you see before bed"
- 13 tags, each ≤20 characters
- 9 mockup prompts using the exact vault structure (custom bedroom variations for this theme)

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
        <pre style="background:#222;color:#0f0;padding:20px;font-family:monospace;white-space:pre-wrap">{{result}}</pre>
        <p>Copy everything above into Etsy. You only approve the draft.</p>
        <a href="/" class="btn btn-success">Generate Another Listing</a>
    </div>
    ''', theme=theme, result=result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
