import sys
import os

# Vercel Path Fixer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import hashlib
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

from core.ai_strength import AIStrength
from core.breach_check import breach_check

ai = AIStrength()
app = FastAPI(title="Password Guard Web")

class PasswordCheckRequest(BaseModel):
    password: str

# ==========================================
# 🌐 ওয়েবসাইটের ফ্রন্টএন্ড (HTML Page)
# ==========================================
@app.get("/", response_class=HTMLResponse)
async def serve_website():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Password Guard | Smart Security</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; text-align: center; padding: 50px 20px; margin: 0; }
            h1 { color: #3b82f6; font-size: 2.5rem; margin-bottom: 10px; }
            p { font-size: 1.1rem; color: #cbd5e1; max-width: 600px; margin: 0 auto 30px; }
            .scanner-box { background: #1e293b; padding: 30px; border-radius: 12px; max-width: 500px; margin: 0 auto; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); }
            input[type="text"] { width: 80%; padding: 12px; border-radius: 6px; border: 1px solid #334155; background: #0f172a; color: white; margin-bottom: 20px; font-size: 1rem; }
            button { background-color: #2563eb; color: white; border: none; padding: 12px 20px; font-size: 1rem; border-radius: 6px; cursor: pointer; transition: 0.3s; margin: 5px; }
            button:hover { background-color: #1d4ed8; }
            .gen-btn { background-color: #10b981; }
            .gen-btn:hover { background-color: #059669; }
            .copy-btn { background-color: #64748b; }
            .copy-btn:hover { background-color: #475569; }
            .result { margin-top: 20px; font-weight: bold; text-align: left; padding: 15px; border-radius: 6px; display: none; }
            
            .downloads { margin-top: 40px; }
            .dl-btn { display: inline-block; margin: 10px; padding: 10px 20px; background: #334155; color: white; text-decoration: none; border-radius: 6px; transition: 0.3s; }
            .dl-btn:hover { background: #475569; }
            
            /* CLI Guide Section Styles */
            .cli-guide { background: #1e293b; padding: 25px; border-radius: 12px; max-width: 600px; margin: 40px auto; text-align: left; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); }
            .cli-guide h3 { color: #38bdf8; margin-top: 0; margin-bottom: 15px; }
            .cli-guide p { margin-left: 0; margin-bottom: 15px; font-size: 1rem; color: #cbd5e1;}
            .code-block { background: #0f172a; padding: 15px; border-radius: 6px; font-family: monospace; color: #a7f3d0; line-height: 1.6; overflow-x: auto; }
            .comment { color: #64748b; }
        </style>
    </head>
    <body>

        <h1>🛡️ Password Guard</h1>
        <p>Advanced AI-powered password protection & vault management. Scan, generate, and secure your digital life completely offline or on the cloud.</p>

        <!-- Scanner UI -->
        <div class="scanner-box">
            <h2>Web Scanner & Generator</h2>
            <input type="text" id="pwdInput" placeholder="Enter or generate password...">
            <br>
            <button onclick="checkPassword()">Scan Password</button>
            <button class="gen-btn" onclick="generatePassword()">🪄 Generate Random</button>
            <button class="copy-btn" onclick="copyPassword()">📋 Copy</button>
            <div id="resultBox" class="result"></div>
        </div>

        <!-- Downloads Section -->
        <div class="downloads">
            <h3>📥 Download Offline App</h3>
            <a href="https://raw.githubusercontent.com/Kiran-mondal/Password-Guard/main/installers/install_linux.sh" class="dl-btn" download>🐧 Linux Installer</a>
            <a href="https://raw.githubusercontent.com/Kiran-mondal/Password-Guard/main/installers/install_termux.sh" class="dl-btn" download>📱 Termux (Android)</a>
            <a href="https://github.com/Kiran-mondal/Password-Guard/archive/refs/heads/main.zip" class="dl-btn">🪟 Windows (ZIP)</a>
        </div>

        <!-- CLI Guide Section -->
        <div class="cli-guide">
            <h3>💻 Terminal / CLI Usage</h3>
            <p>After downloading, you can run the app completely offline via terminal for maximum privacy:</p>
            <div class="code-block">
                <span class="comment"># Scan a password securely</span><br>
                <code>python main.py --scan "your_password"</code><br><br>
                
                <span class="comment"># Generate a strong 16-char password</span><br>
                <code>python main.py --generate</code><br><br>
                
                <span class="comment"># Scan device for saved browser passwords</span><br>
                <code>python main.py --devicescan</code>
            </div>
        </div>

        <!-- JavaScript -->
        <script>
            function generatePassword() {
                const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+";
                let password = "";
                for (let i = 0; i < 16; i++) {
                    password += chars.charAt(Math.floor(Math.random() * chars.length));
                }
                document.getElementById("pwdInput").value = password;
                checkPassword(); 
            }

            function copyPassword() {
                const pwd = document.getElementById("pwdInput").value;
                if(!pwd) { alert("Nothing to copy!"); return; }
                navigator.clipboard.writeText(pwd);
                alert("Password copied to clipboard! (Saved)");
            }

            async function checkPassword() {
                const pwd = document.getElementById("pwdInput").value;
                const resultBox = document.getElementById("resultBox");
                if(!pwd) { alert("Please enter a password!"); return; }

                resultBox.style.display = "block";
                resultBox.style.backgroundColor = "#334155";
                resultBox.innerHTML = "Scanning on Cloud Database... ⏳";

                try {
                    const response = await fetch("/api/scan", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ password: pwd })
                    });
                    
                    const data = await response.json();
                    
                    if(data.leaked) {
                        resultBox.style.backgroundColor = "#7f1d1d";
                        resultBox.innerHTML = `🚨 <b>CRITICAL ALERT:</b> Password found in leaks!<br><br><b>AI Score:</b> ${data.ai_score}/100<br><b>Tips:</b> ${data.suggestions.join(', ')}`;
                    } else if(data.ai_score < 70) {
                        resultBox.style.backgroundColor = "#9a3412";
                        resultBox.innerHTML = `⚠️ <b>Safe, but Weak.</b><br><br><b>AI Score:</b> ${data.ai_score}/100<br><b>Tips:</b> ${data.suggestions.join(', ')}`;
                    } else {
                        resultBox.style.backgroundColor = "#14532d";
                        resultBox.innerHTML = `✅ <b>Safe & Strong!</b><br><br><b>AI Score:</b> ${data.ai_score}/100<br>No leaks found.`;
                    }
                } catch(err) {
                    resultBox.innerHTML = "❌ Error connecting to server.";
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# ==========================================
# ⚙️ ওয়েবসাইটের ব্যাকএন্ড API (Serverless)
# ==========================================
@app.post("/api/scan")
async def scan_password(req: PasswordCheckRequest):
    pwd = req.password
    
    strength_data = ai.analyze(pwd)
    is_leaked = breach_check(pwd)
    
    pwd_hash = hashlib.sha256(pwd.encode()).hexdigest()
    
    try:
        from cloud.neon_db import get_db_connection
        conn = await get_db_connection()
        if conn:
            await conn.execute("""
                INSERT INTO scan_logs (password_hash, strength_score, is_leaked)
                VALUES ($1, $2, $3)
            """, pwd_hash, strength_data["score"], is_leaked)
            await conn.close() 
    except Exception as e:
        pass # সার্ভারলেস লগিং ফেইল করলে ক্র্যাশ ঠেকানোর জন্য
    
    return {
        "status": "success",
        "leaked": is_leaked,
        "ai_score": strength_data["score"],
        "entropy": strength_data["entropy"],
        "suggestions": strength_data["suggestion"]
    }
    
