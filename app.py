from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# واجهة الروبوت فارس المطور (UI/UX)
HTML_UI = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>الروبوت فارس - الصديق الذكي</title>
    <style>
        body { background:#121212; color:white; font-family:sans-serif; text-align:center; padding-top:20px; }
        .bot-container { background:#1e1e1e; width:90%; max-width:400px; margin:0 auto; padding:20px; border-radius:20px; border: 2px solid #007bff; }
        #avatar { width:130px; border-radius:50%; background:#333; margin-bottom:10px; transition: 0.5s; }
        #chat-display { height:250px; overflow-y:auto; background:#000; padding:15px; border-radius:10px; margin:15px 0; text-align:right; border: 1px solid #444; }
        input { width:70%; padding:12px; border-radius:8px; border:none; outline:none; }
        button { padding:12px; background:#007bff; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:bold; }
        .msg-user { color: #aaa; margin-bottom: 5px; }
        .msg-bot { color: #007bff; margin-bottom: 10px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="bot-container">
        <img id="avatar" src="https://api.dicebear.com/7.x/bottts/svg?seed=Fares&mood=happy" alt="Fares Bot">
        <h3>المطور فارس: الروبوت الصديق</h3>
        <div id="chat-display"></div>
        <input type="text" id="user-input" placeholder="أهدر مع فارس...">
        <button onclick="talkToBot()">إرسال</button>
    </div>

    <script>
        function talkToBot() {
            let input = document.getElementById('user-input');
            let msg = input.value;
            if(!msg) return;

            let chat = document.getElementById('chat-display');
            chat.innerHTML += `<div class="msg-user">أنت: ${msg}</div>`;
            
            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: msg})
            })
            .then(res => res.json())
            .then(data => {
                chat.innerHTML += `<div class="msg-bot">فارس: ${data.reply}</div>`;
                document.getElementById('avatar').src = data.img;
                chat.scrollTop = chat.scrollHeight;
                input.value = '';
                
                // ميزة النطق الصوتي (Text-to-Speech)
                let speech = new SpeechSynthesisUtterance(data.reply);
                speech.lang = 'ar-SA';
                window.speechSynthesis.speak(speech);
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_UI)

@app.route('/chat', methods=['POST'])
def chat_logic():
    data = request.get_json()
    user_text = data.get('text', '').lower()
    
    # برمجة شخصية الروبوت فارس (Logic)
    if "يضحك" in user_text or "قسر" in user_text:
        reply = "ههه، راني نقسر معاك! واش راك يا صاحبي؟"
        img = "https://api.dicebear.com/7.x/bottts/svg?seed=Fares&mood=happy"
    elif "مطور" in user_text or "شكون خدمك" in user_text:
        reply = "أنا الروبوت فارس، المطور العالمي فارس هو اللي برمجني!"
        img = "https://api.dicebear.com/7.x/bottts/svg?seed=Fares&eyes=glow"
    elif "سلام" in user_text or "صباح الخير" in user_text:
        reply = "أهلاً بيك يا خويا، واش كاين جديد اليوم؟"
        img = "https://api.dicebear.com/7.x/bottts/svg?seed=Fares"
    else:
        reply = "والله هدرة شابة، زيد قولي كاش عفسة وحدوخرة!"
        img = "https://api.dicebear.com/7.x/bottts/svg?seed=Fares"

    return jsonify({'reply': reply, 'img': img})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
