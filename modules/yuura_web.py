from flask import Flask, render_template_string, request
import os
import subprocess

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Yuura OS - Web Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background-color: #0f172a; color: #38bdf8; font-family: monospace; padding: 20px; }
        h1 { color: #f43f5e; text-align: center; text-shadow: 0 0 10px rgba(244,63,94,0.5); }
        .card { background: #1e293b; border: 1px solid #334155; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
        input[type="text"] { width: 70%; padding: 10px; background: #0f172a; border: 1px solid #38bdf8; color: #fff; border-radius: 4px; }
        button { padding: 10px 20px; background: #38bdf8; color: #0f172a; border: none; font-weight: bold; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0ea5e9; }
        pre { background: #020617; padding: 10px; border-radius: 4px; color: #4ade80; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>YUURA OS // WEB CONTROL ROOM</h1>
    <div class="card">
        <h3>[+] Jalankan Perintah Sistem</h3>
        <form method="POST">
            <input type="text" name="command" placeholder="Ketik perintah (cth: ls, uname -a, dll)..." required>
            <button type="submit">Kirim Eksekusi</button>
        </form>
    </div>
    
    {% if command %}
    <div class="card">
        <h3>[i] Output Perintah: <code>{{ command }}</code></h3>
        <pre>{{ output }}</pre>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    command = ""
    if request.method == "POST":
        command = request.form.get("command")
        try:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            output = result
        except Exception as e:
            output = str(e)
    return render_template_string(HTML_TEMPLATE, output=output, command=command)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
