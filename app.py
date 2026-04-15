import os
from flask import Flask, request, jsonify, render_template_string
import yt_dlp
import google.generativeai as genai

app = Flask(__name__)

# AI Key (Tumhari set hai)
API_KEY = "AIzaSyAunX4Q9HR-4VCh6CemgDdm_FfAGPievPU"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Youtub | Premium Tool</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #080808; color: #ffffff; font-family: "Inter", sans-serif; }
        .youtub-red { color: #FF0000; }
        .youtub-card { background: #161616; border: 1px solid #222; border-radius: 20px; transition: 0.3s; }
        .youtub-input { background: #000 !important; border: 1px solid #333 !important; color: white !important; border-radius: 12px !important; transition: 0.3s; }
        .youtub-input:focus { border-color: #FF0000 !important; box-shadow: 0 0 10px rgba(255, 0, 0, 0.2); }
        .btn-main { background: #FF0000; color: white; border-radius: 12px; font-weight: 800; transition: 0.3s; text-transform: uppercase; letter-spacing: 1px; }
        .btn-main:active { transform: scale(0.95); opacity: 0.8; }
        .btn-ai { background: #ffffff; color: #000; border-radius: 12px; font-weight: 800; transition: 0.3s; }
    </style>
</head>
<body class="p-6">

    <header class="flex flex-col items-center justify-center py-10">
        <div class="flex items-center gap-2 mb-2">
            <i class="fab fa-youtube text-5xl youtub-red"></i>
            <h1 class="text-4xl font-black tracking-tighter italic">Youtub</h1>
        </div>
        <p class="text-gray-500 text-xs tracking-[0.3em] uppercase">The Ultimate Stealth Tool</p>
    </header>

    <div class="max-w-md mx-auto space-y-8">
        
        <div class="youtub-card p-8">
            <h2 class="text-sm font-bold mb-6 text-gray-400 uppercase tracking-widest"><i class="fas fa-bolt mr-2 youtub-red"></i> Media Downloader</h2>
            <input type="text" id="v_url" placeholder="Paste link here..." class="youtub-input w-full p-4 mb-4 outline-none">
            <button onclick="handleDL()" id="dl_btn" class="w-full py-4 btn-main shadow-lg shadow-red-600/20">Get Media Link</button>
            <div id="dl_res" class="mt-4 hidden p-4 bg-red-600/10 border border-red-600/20 rounded-xl text-center text-sm font-bold"></div>
        </div>

        <div class="youtub-card p-8">
            <h2 class="text-sm font-bold mb-6 text-gray-400 uppercase tracking-widest"><i class="fas fa-robot mr-2 text-white"></i> AI Brain</h2>
            <textarea id="ai_q" rows="4" placeholder="Ask Youtub AI anything..." class="youtub-input w-full p-4 mb-4 outline-none resize-none"></textarea>
            <button onclick="handleAI()" id="ai_btn" class="w-full py-4 btn-ai shadow-lg shadow-white/10">Ask AI Assistant</button>
            <div id="ai_res" class="mt-4 hidden p-4 bg-gray-900 border border-gray-800 rounded-xl text-sm text-gray-400 leading-relaxed"></div>
        </div>

    </div>

    <footer class="mt-20 text-center text-gray-700 text-[10px] tracking-widest uppercase">
        <p>© 2026 YOUTUB STUDIO • SIKAR RAJASTHAN</p>
    </footer>

    <script>
        async function handleDL() {
            const u = document.getElementById('v_url').value;
            const res = document.getElementById('dl_res');
            if(!u) return;
            res.innerHTML = "⚡ ANALYZING LINK..."; res.classList.remove('hidden');
            try {
                const r = await fetch('/dl', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({url:u})});
                const d = await r.json();
                res.innerHTML = d.ok ? `<a href="${d.link}" target="_blank" class="youtub-red underline font-black">🔥 CLICK TO DOWNLOAD</a>` : "❌ LINK ERROR OR PRIVATE";
            } catch(e) { res.innerHTML = "⚠️ SYSTEM OVERLOAD"; }
        }

        async function handleAI() {
            const q = document.getElementById('ai_q').value;
            const res = document.getElementById('ai_res');
            if(!q) return;
            res.innerHTML = "🧬 GENERATING ANSWER..."; res.classList.remove('hidden');
            try {
                const r = await fetch('/ai', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({q:q})});
                const d = await r.json();
                res.innerHTML = d.ok ? d.ans : "⚠️ AI IS SLEEPING";
            } catch(e) { res.innerHTML = "⚠️ NO INTERNET"; }
        }
    </script>
</body>
</html>
"""

# --- ROUTES ---
@app.route('/')
def home(): return render_template_string(HTML_CODE)

@app.route('/dl', methods=['POST'])
def handle_dl():
    url = request.json.get('url')
    try:
        ydl_opts = {'format': 'best', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({'ok': True, 'link': info.get('url')})
    except: return jsonify({'ok': False})

@app.route('/ai', methods=['POST'])
def handle_ai():
    q = request.json.get('q')
    try:
        response = model.generate_content(q)
        return jsonify({'ok': True, 'ans': response.text})
    except: return jsonify({'ok': False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
