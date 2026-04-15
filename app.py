import os
from flask import Flask, request, jsonify, render_template_string
import yt_dlp

app = Flask(__name__)

# --- BINA AI WALA SIMPLE LOOK ---
HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head><link rel="icon" type="image/x-icon" href="https://www.youtube.com/s/desktop/28e6783d/img/favicon.ico">
<link rel="apple-touch-icon" href="https://www.youtube.com/s/desktop/28e6783d/img/favicon_144x144.png">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Youtub downloader</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #000; color: #fff; font-family: sans-serif; }
        .yt-red { color: #ff0000; }
        .main-box { background: #111; border: 1px solid #222; border-radius: 24px; }
        .input-style { background: #000 !important; border: 1px solid #333 !important; color: #fff !important; border-radius: 12px; }
        .btn-dl { background: #ff0000; color: #fff; font-weight: 800; border-radius: 12px; transition: 0.3s; }
        .btn-dl:active { transform: scale(0.98); }
    </style>
</head>
<body class="flex flex-col items-center justify-center min-h-screen p-6">

    <div class="flex items-center gap-2 mb-10">
        <i class="fab fa-youtube text-5xl yt-red"></i>
        <h1 class="text-4xl font-black italic">Youtub</h1>
    </div>

    <div class="w-full max-w-md main-box p-8 shadow-2xl shadow-red-900/10">
        <h2 class="text-lg font-bold mb-6 text-center text-gray-400 uppercase tracking-widest">Video Downloader</h2>
        
        <input type="text" id="v_url" placeholder="Paste Video Link Here..." 
            class="w-full p-4 mb-4 input-style outline-none focus:border-red-600">
            
        <button onclick="extractLink()" id="btn" class="w-full py-4 btn-dl shadow-lg shadow-red-600/20 uppercase">
            Get Download Link
        </button>

        <div id="res" class="mt-6 hidden p-4 rounded-xl bg-white/5 border border-white/10 text-center text-sm">
            </div>
    </div>

    <p class="mt-10 text-gray-600 text-[10px] uppercase tracking-widest">© 2026 Youtub Studio</p>

    <script>
        async function extractLink() {
            const url = document.getElementById('v_url').value;
            const res = document.getElementById('res');
            const btn = document.getElementById('btn');

            if(!url) return alert("Bhai, pehle link toh dalo!");

            res.innerHTML = "⚡ Working on it...";
            res.classList.remove('hidden');
            btn.disabled = true;

            try {
                const response = await fetch('/dl', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                });
                const data = await response.json();
                
                if(data.ok) {
                    res.innerHTML = `<div class='mb-2 text-green-500 font-bold'>Video Ready!</div>
                                     <a href="${data.link}" target="_blank" class="text-blue-400 font-black underline text-lg">🔥 CLICK TO DOWNLOAD</a>`;
                } else {
                    res.innerHTML = "❌ Error: Link expired or video is private.";
                }
            } catch(e) {
                res.innerHTML = "⚠️ Server busy. Try again.";
            }
            btn.disabled = false;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

@app.route('/dl', methods=['POST'])
def handle_dl():
    url = request.json.get('url')
    try:
        # Extra options taaki Render par block na ho
        ydl_opts = {
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({'ok': True, 'link': info.get('url')})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'ok': False})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
