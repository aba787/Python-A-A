
from flask import Flask, request, jsonify
import logging
import sys
import traceback
from datetime import datetime

# إعداد التسجيل المفصل
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <title>🔧 Debug Chatbot - تشخيص المشاكل</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border-radius: 15px;
                padding: 30px;
            }
            .chat { 
                border: 2px solid rgba(255,255,255,0.3); 
                padding: 20px; 
                height: 400px; 
                overflow-y: scroll; 
                margin: 20px 0; 
                background: rgba(0,0,0,0.1);
                border-radius: 10px;
            }
            .user { color: #4ecdc4; margin: 15px 0; padding: 10px; background: rgba(78,205,196,0.2); border-radius: 8px; }
            .bot { color: #96ceb4; margin: 15px 0; padding: 10px; background: rgba(150,206,180,0.2); border-radius: 8px; }
            .error { color: #ff6b6b; margin: 15px 0; padding: 10px; background: rgba(255,107,107,0.2); border-radius: 8px; }
            .success { color: #51cf66; margin: 15px 0; padding: 10px; background: rgba(81,207,102,0.2); border-radius: 8px; }
            input { 
                width: 70%; 
                padding: 12px; 
                border: 2px solid rgba(255,255,255,0.3); 
                border-radius: 25px; 
                background: rgba(255,255,255,0.1);
                color: white;
                font-size: 16px;
            }
            input::placeholder { color: rgba(255,255,255,0.7); }
            button { 
                padding: 12px 25px; 
                margin-left: 10px; 
                border: none; 
                border-radius: 25px; 
                background: linear-gradient(45deg, #ff6b6b, #4ecdc4); 
                color: white; 
                cursor: pointer; 
                font-size: 16px;
                font-weight: bold;
            }
            button:hover { transform: scale(1.05); }
            .status { 
                text-align: center; 
                margin: 20px 0; 
                padding: 15px; 
                background: rgba(255,255,255,0.1); 
                border-radius: 10px; 
            }
            .debug-info {
                margin: 20px 0;
                padding: 15px;
                background: rgba(0,0,0,0.2);
                border-radius: 10px;
                font-family: monospace;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔧 Debug Chatbot - نسخة التشخيص</h1>
            <div class="status">
                <strong>✅ الخادم يعمل بنجاح!</strong><br>
                الوقت: <span id="time"></span><br>
                عدد الرسائل المرسلة: <span id="messageCount">0</span>
            </div>
            
            <div id="chat" class="chat">
                <div class="success">
                    <strong>🚀 مرحباً!</strong> هذا تطبيق تشخيص مبسط للتأكد من عمل الخادم.
                    <br>اكتب أي رسالة لاختبار الاتصال.
                </div>
            </div>
            
            <input type="text" id="message" placeholder="اكتب رسالتك هنا...">
            <button onclick="sendMessage()">📤 إرسال</button>
            <button onclick="testConnection()">🔍 اختبار الاتصال</button>
            <button onclick="clearChat()">🗑️ مسح</button>
            
            <div class="debug-info">
                <strong>📊 معلومات التشخيص:</strong>
                <div id="debugInfo">جاهز للاختبار...</div>
            </div>
        </div>
        
        <script>
            let messageCount = 0;
            
            function updateTime() {
                document.getElementById('time').textContent = new Date().toLocaleString('ar-SA');
            }
            setInterval(updateTime, 1000);
            updateTime();
            
            async function sendMessage() {
                const message = document.getElementById('message').value.trim();
                const chat = document.getElementById('chat');
                const debugInfo = document.getElementById('debugInfo');
                
                if (!message) {
                    addToChat('error', '❌ يرجى كتابة رسالة أولاً!');
                    return;
                }
                
                // عرض رسالة المستخدم
                addToChat('user', `👤 أنت: ${message}`);
                document.getElementById('message').value = '';
                messageCount++;
                document.getElementById('messageCount').textContent = messageCount;
                
                try {
                    debugInfo.innerHTML = '🔄 جاري الإرسال...';
                    const startTime = Date.now();
                    
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({message: message})
                    });
                    
                    const responseTime = Date.now() - startTime;
                    debugInfo.innerHTML = `📡 حالة الاستجابة: ${response.status}<br>⏱️ وقت الاستجابة: ${responseTime}ms`;
                    
                    if (response.ok) {
                        const data = await response.json();
                        addToChat('bot', `🤖 البوت: ${data.response}`);
                        addToChat('success', `✅ تم الإرسال بنجاح! (${responseTime}ms)`);
                        debugInfo.innerHTML += `<br>📊 البيانات: ${JSON.stringify(data).substring(0,100)}...`;
                    } else {
                        const errorText = await response.text();
                        addToChat('error', `❌ خطأ ${response.status}: ${errorText}`);
                        debugInfo.innerHTML += `<br>🚨 تفاصيل الخطأ: ${errorText}`;
                    }
                    
                } catch (error) {
                    addToChat('error', `💥 خطأ في الشبكة: ${error.message}`);
                    debugInfo.innerHTML = `❌ خطأ اتصال: ${error.message}`;
                    console.error('Network Error:', error);
                }
            }
            
            async function testConnection() {
                const debugInfo = document.getElementById('debugInfo');
                try {
                    debugInfo.innerHTML = '🧪 اختبار الاتصال...';
                    
                    const response = await fetch('/health');
                    const data = await response.json();
                    
                    if (response.ok) {
                        addToChat('success', `✅ اختبار الاتصال نجح! الخادم يعمل بشكل طبيعي.`);
                        debugInfo.innerHTML = `✅ الاتصال سليم<br>📊 حالة الخدمة: ${data.status}`;
                    } else {
                        addToChat('error', `⚠️ مشكلة في اختبار الاتصال: ${response.status}`);
                    }
                } catch (error) {
                    addToChat('error', `❌ فشل اختبار الاتصال: ${error.message}`);
                    debugInfo.innerHTML = `❌ فشل الاتصال: ${error.message}`;
                }
            }
            
            function addToChat(type, message) {
                const chat = document.getElementById('chat');
                const div = document.createElement('div');
                div.className = type;
                div.innerHTML = message;
                chat.appendChild(div);
                chat.scrollTop = chat.scrollHeight;
            }
            
            function clearChat() {
                document.getElementById('chat').innerHTML = `
                    <div class="success">
                        <strong>🚀 تم مسح المحادثة!</strong> جاهز لاختبارات جديدة.
                    </div>
                `;
                messageCount = 0;
                document.getElementById('messageCount').textContent = messageCount;
            }
            
            // السماح بالإرسال بالزر Enter
            document.getElementById('message').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') sendMessage();
            });
            
            // اختبار تلقائي عند التحميل
            setTimeout(testConnection, 1000);
        </script>
    </body>
    </html>
    '''

@app.route('/chat', methods=['POST'])
def chat():
    try:
        print(f"🎯 [{datetime.now()}] تم استلام طلب في /chat")
        
        # فحص نوع المحتوى
        if not request.is_json:
            print("❌ الطلب ليس JSON")
            return jsonify({'error': 'الطلب يجب أن يكون JSON', 'received_content_type': request.content_type}), 400
        
        data = request.get_json()
        print(f"📨 البيانات المستلمة: {data}")
        
        if not data or 'message' not in data:
            print("❌ لا توجد رسالة في البيانات")
            return jsonify({'error': 'الرسالة مطلوبة', 'received_data': str(data)}), 400
        
        user_message = data['message']
        print(f"👤 رسالة المستخدم: '{user_message}'")
        
        # معالجة بسيطة للرسائل
        if "مرحبا" in user_message.lower() or "hello" in user_message.lower():
            response = "🌟 أهلاً وسهلاً! التطبيق يعمل بشكل ممتاز!"
        elif "وقت" in user_message.lower() or "time" in user_message.lower():
            response = f"⏰ الوقت الآن: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        elif "اختبار" in user_message.lower() or "test" in user_message.lower():
            response = "✅ اختبار نجح! الخادم يستجيب بشكل طبيعي."
        else:
            response = f"✨ تم استلام رسالتك: '{user_message}'. النظام يعمل بكفاءة عالية!"
        
        print(f"🤖 الرد المرسل: {response}")
        
        return jsonify({
            'response': response,
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'received_message': user_message,
            'message_length': len(user_message)
        })
        
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"💥 خطأ في /chat: {str(e)}")
        print(f"🔍 تفاصيل الخطأ:\n{error_details}")
        
        return jsonify({
            'error': f'خطأ داخلي: {str(e)}',
            'details': 'تحقق من سجلات الخادم',
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'debug_chatbot',
        'timestamp': datetime.now().isoformat(),
        'uptime': 'running',
        'port': 5000,
        'host': '0.0.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'المسار غير موجود',
        'available_routes': ['/', '/chat', '/health'],
        'timestamp': datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'خطأ داخلي في الخادم',
        'message': 'تم تسجيل الخطأ وسيتم إصلاحه',
        'timestamp': datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    print("🚀" + "="*50)
    print("🔧 بدء تشغيل تطبيق التشخيص المبسط")
    print("📍 سيعمل على: http://0.0.0.0:5000")
    print("🔍 اختبار الصحة: http://0.0.0.0:5000/health")
    print("💬 واجهة التشخيص: http://0.0.0.0:5000")
    print("="*50)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False,  # منع إعادة التحميل المتكررة
            threaded=True
        )
    except Exception as e:
        print(f"❌ خطأ في تشغيل التطبيق: {e}")
        traceback.print_exc()
