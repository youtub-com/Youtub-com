import os
from flask import Flask, request, jsonify, render_template_string
import yt_dlp
import google.generativeai as genai

app = Flask(__name__)

# API KEY
API_KEY = "AIzaSyAunX4Q9HR-4VCh6CemgDdm_FfAGPievPU"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

HTML_CODE = """
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ULTRA TOOLS | AI & MEDIA</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root { --primary: #00f2fe; --secondary: #4facfe; }
        body { background: #020617; color: white; font-family: 'Inter', sans-serif; }
        .neon-border { border: 1px solid rgba(0, 242, 254, 0.3); box-shadow: 0 0 15px rgba(0, 242, 254, 0.1); }
        .glass { background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(12px); border-radius: 28px; }
        .gradient-btn { background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%); color: #000; font-weight: 800; transition: 0.4s; }
        .gradient-btn:hover { box-shadow: 0 0 25px rgba(0, 242, 254, 0.5); transform: translateY(-2px); }
        .tab-active { border-bottom: 3px solid var(--primary); color: var(--primary); }
        input, textarea { background: rgba(0,0,0,0.4) !important; border: 1px solid #1e293b !important; color: white !important; }
        input:focus { border-color: var(--primary) !important; box-shadow: 0 0 10px rgba(0, 242, 254, 0.2); }
    </style>
</head>
<body class="min-h-screen pb-10">

    <nav class="p-6 flex justify-between items-center glass m-4 neon-border sticky top-4 z-50">
        <span class="text-xl font-black tracking-tighter gradient-text" style="background: linear-gradient(to right, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">ULTRA.UNQ</span>
        <div class="flex gap-4">
            <i class="fas fa-shield-alt text-blue-400"></i>
            <i class="fas fa-bolt text-yellow-400"></i>
        </div>
    </nav>

    <div class="max-w-md mx-auto px-4 mt-8 space-y-8">
        
        <div class="glass p-8 neon-border">
            <div class="flex items-center gap-3 mb-6">
                <div class="p-3 bg-blue-500/10 rounded-2xl"><i class="fas fa-cloud-download-alt text-blue-400 text-xl"></i></div>
                <h2 class="text-xl font-extrabold tracking-tight">Media Saver</h2>
            </div>
            <p class="text-gray-400 text-sm mb-4">Paste any link from Instagram or YouTube</p>
            <input type="text" id="v_url" placeholder="https://..." class="w-full p-4 rounded-2xl mb-4 text-sm focus:outline-none">
            <button onclick="handleDL()" id="dl_btn" class="w-full py-4 rounded-2xl gradient-btn uppercase tracking-widest text-xs">Fetch Video</button>
            <div id="dl_res" class="mt-6 hidden p-4 rounded-2xl bg-blue-900/20 border border-blue-500/30 text-center animate-pulse"></div>
        </div>

        <div class="glass p-8 neon-border">
            <div class="flex items-center gap-3 mb-6">
                <div class="p-3 bg-purple-500/10 rounded-2xl"><i class="fas fa-brain text-purple-400 text-xl"></i></div>
                <h2 class="text-xl font-extrabold tracking-tight">AI Mastermind</h2>
            </div>
            <textarea id="ai_q" rows="4" placeholder="Ask me anything..." class="w-full p-4 rounded-2xl mb-4 text-sm focus:outline-none resize-none"></textarea>
            <button onclick="handleAI()" id="ai_btn" class="w-full py-4 rounded-2xl gradient-btn uppercase tracking-widest text-xs" style="background: linear-gradient(135deg, #a78bfa, #8b5cf6);">Consult AI</button>
            <div id="ai_res" class="mt-6 hidden p-5 rounded-2xl bg-white/5 border border-white/10 text-sm text-gray-300 leading-relaxed overflow-hidden"></div>
        </div>

    </div>

    <script>
        async function handleDL() {
            const u = document.getElementById('v_url').value;
            const res = document.getElementById('dl_res');
            if(!u) return;
            res.innerHTML = "⚡ PROCESSING..."; res.classList.remove('hidden');
            try {
                const r = await fetch('/dl', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({url:u})});
                const d = await r.json();
                res.classList.remove('animate-pulse');
                res.innerHTML = d.ok ? `<a href="${d.link}" target="_blank" class="text-cyan-400 font-black">🔥 DOWNLOAD NOW</a>` : "❌ LINK EXPIRED/INVALID";
            } catch(e) { res.innerHTML = "⚠️ SERVER BUSY"; }
        }

        async function handleAI() {
            const q = document.getElementById('ai_q').value;
            const res = document.getElementById('ai_res');
            if(!q) return;
            res.innerHTML = "🧬 THINKING..."; res.classList.remove('hidden');
            try {
                const r = await fetch('/ai', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({q:q})});
                const d = await r.json();
                res.innerHTML = d.ok ? d.ans : "⚠️ AI ERROR";
            } catch(e) { res.innerHTML = "⚠️ OFFLINE"; }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return render_template_string(HTML_CODE)

@app.route('/dl', methods=['POST'])
def handle_dl():
    url = request.json.get('url')
    try:
        with yt_dlp.YoutubeDL({'format': 'best', 'quiet': True}) as ydl:
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
