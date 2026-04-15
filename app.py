from flask import Flask, request, jsonify, render_template_string
import yt_dlp
import google.generativeai as genai

# --- CONFIGURATION ---
# अपनी फ्री API Key यहाँ डालें (Google AI Studio से मिलेगी)
API_KEY = "AIzaSyAunX4Q9HR-4VCh6CemgDdm_FfAGPievPU"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)

# --- HTML FRONTEND (Embedded for Mobile Ease) ---
HTML_CODE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartTools | AI & Downloader</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #0f172a; color: white; font-family: sans-serif; }
        .glass { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; }
        .gradient-text { background: linear-gradient(90deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    </style>
</head>
<body class="p-4 flex flex-col items-center">

    <header class="text-center my-10">
        <h1 class="text-4xl font-black gradient-text">SMART TOOLS</h1>
        <p class="text-gray-400 mt-2">No Identity. Pure Utility.</p>
    </header>

    <div class="w-full max-w-md space-y-6">
        
        <div class="glass p-6">
            <h2 class="text-lg font-bold mb-4">📹 Video Downloader</h2>
            <input type="text" id="v_url" placeholder="Paste URL..." class="w-full p-3 rounded-lg bg-gray-900 border border-gray-700 mb-3 focus:outline-none focus:border-blue-500">
            <button onclick="dl()" id="dl_btn" class="w-full py-3 bg-blue-600 rounded-lg font-bold">Get Link</button>
            <div id="dl_res" class="mt-4 hidden text-sm text-center bg-blue-900/20 p-3 rounded-lg"></div>
        </div>

        <div class="glass p-6">
            <h2 class="text-lg font-bold mb-4">🤖 AI Assistant</h2>
            <textarea id="ai_q" rows="3" placeholder="Ask anything..." class="w-full p-3 rounded-lg bg-gray-900 border border-gray-700 mb-3 focus:outline-none focus:border-purple-500"></textarea>
            <button onclick="ask()" id="ai_btn" class="w-full py-3 bg-purple-600 rounded-lg font-bold">Generate</button>
            <div id="ai_res" class="mt-4 hidden text-sm bg-gray-900 p-3 rounded-lg border border-gray-700 whitespace-pre-wrap"></div>
        </div>

    </div>

    <script>
        async function dl() {
            const u = document.getElementById('v_url').value;
            const res = document.getElementById('dl_res');
            res.innerHTML = "Processing..."; res.classList.remove('hidden');
            
            const r = await fetch('/dl', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url: u})
            });
            const d = await r.json();
            res.innerHTML = d.ok ? `<a href="${d.link}" class="text-blue-400 font-bold">Download Found! Click Here</a>` : "Error: Link not found.";
        }

        async function ask() {
            const q = document.getElementById('ai_q').value;
            const res = document.getElementById('ai_res');
            res.innerHTML = "Thinking..."; res.classList.remove('hidden');

            const r = await fetch('/ai', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({q: q})
            });
            const d = await r.json();
            res.innerHTML = d.ok ? d.ans : "AI Error.";
        }
    </script>
</body>
</html>
"""

# --- ROUTES ---

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/dl', methods=['POST'])
def handle_dl():
    url = request.json.get('url')
    try:
        with yt_dlp.YoutubeDL({'format': 'best', 'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({'ok': True, 'link': info.get('url')})
    except:
        return jsonify({'ok': False})

@app.route('/ai', methods=['POST'])
def handle_ai():
    q = request.json.get('q')
    try:
        response = model.generate_content(q)
        return jsonify({'ok': True, 'ans': response.text})
    except:
        return jsonify({'ok': False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
