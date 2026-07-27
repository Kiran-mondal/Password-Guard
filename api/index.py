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
            .dl-btn { display: inline-block; margin: 10px; padding: 10px 20px; background: #334155; color: white; text-decoration: none; border-radius: 6px; transition: 0.3s; cursor: pointer; border: 1px solid #475569; }
            .dl-btn:hover { background: #475569; }
            
            /* CLI Guide Section Styles (Hidden initially) */
            .cli-guide { display: none; background: #1e293b; padding: 25px; border-radius: 12px; max-width: 600px; margin: 40px auto; text-align: left; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); animation: fadeIn 0.4s ease-in-out; }
            .cli-guide h3 { color: #38bdf8; margin-top: 0; margin-bottom: 10px; }
            .cli-guide p { margin-left: 0; margin-bottom: 15px; font-size: 1rem; color: #cbd5e1;}
            
            .code-box-container { position: relative; background: #0f172a; border-radius: 6px; margin-bottom: 20px; border: 1px solid #334155;}
            .code-block { padding: 15px 70px 15px 15px; font-family: monospace; color: #a7f3d0; line-height: 1.6; overflow-x: auto; white-space: pre-wrap; font-size: 0.95rem; }
            .small-copy-btn { position: absolute; right: 10px; top: 10px; background: #3b82f6; color: white; border: none; padding: 5px 10px; font-size: 0.8rem; border-radius: 4px; cursor: pointer; transition: 0.2s;}
            .small-copy-btn:hover { background: #2563eb; }
            .comment { color: #64748b; }

            @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
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
            <button class="copy-btn" onclick="copyPassword('pwdInput')">📋 Copy</button>
            <div id="resultBox" class="result"></div>
        </div>

        <!-- CLI App Section -->
        <div class="downloads">
            <h3>💻 Install Offline CLI App</h3>
            <!-- No direct downloads. Click opens the guide. -->
            <button class="dl-btn" onclick="showInstallGuide('linux')">🐧 Linux</button>
            <button class="dl-btn" onclick="showInstallGuide('termux')">📱 Termux</button>
            <button class="dl-btn" onclick="showInstallGuide('windows')">🪟 Windows</button>
        </div>

        <!-- Dynamic Install & Usage Guide Section -->
        <div id="cliGuide" class="cli-guide">
            <h3 id="osTitle">Terminal Installation</h3>
            <p>Run the following command in your terminal to install the tool:</p>
            
            <!-- Install Command Box -->
            <div class="code-box-container">
                <button class="small-copy-btn" onclick="copyText('installCommand')">Copy</button>
                <div id="installCommand" class="code-block"></div>
            </div>

            <h3>🚀 How to use it</h3>
            <p>After installation, use these commands to run it completely offline:</p>
            <div class="code-box-container">
                <button class="small-copy-btn" onclick="copyText('usageCommand')">Copy</button>
                <div id="usageCommand" class="code-block"><span class="comment"># Scan a password</span>
python main.py --scan "your_password"

<span class="comment"># Generate a strong password</span>
python main.py --generate

<span class="comment"># Scan device for saved browser passwords</span>
python main.py --devicescan</div>
            </div>
        </div>

        <!-- JavaScript -->
        <script>
            // Platform specific installation commands
            const installCmds = {
                linux: "curl -sO https://raw.githubusercontent.com/Kiran-mondal/Password-Guard/main/installers/install_linux.sh && bash install_linux.sh",
                termux: "curl -sO https://raw.githubusercontent.com/Kiran-mondal/Password-Guard/main/installers/install_termux.sh && bash install_termux.sh",
                windows: "git clone https://github.com/Kiran-mondal/Password-Guard.git\\ncd Password-Guard\\npip install -r requirements.txt"
            };

            const osTitles = {
                linux: "🐧 Linux Terminal Installation",
                termux: "📱 Termux (Android) Installation",
                windows: "🪟 Windows CMD / PowerShell"
            };

            function showInstallGuide(os) {
                const guide = document.getElementById("cliGuide");
                document.getElementById("osTitle").innerText = osTitles[os];
                document.getElementById("installCommand").innerText = installCmds[os];
                
                guide.style.display = "block";
                setTimeout(() => {
                    guide.scrollIntoView({ behavior: "smooth" });
                }, 100);
            }

            function copyText(elementId) {
                let textToCopy = "";
                if(elementId === 'pwdInput') {
                    textToCopy = document.getElementById(elementId).value;
                    if(!textToCopy) { alert("Nothing to copy!"); return; }
                } else {
                    textToCopy = document.getElementById(elementId).innerText;
                }
                
                navigator.clipboard.writeText(textToCopy);
                alert("Copied to clipboard!");
            }

            function generatePassword() {
                const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+";
                let password = "";
                for (let i = 0; i < 16; i++) {
                    password += chars.charAt(Math.floor(Math.random() * chars.length));
                }
                document.getElementById("pwdInput").value = password;
                checkPassword(); 
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
        pass 
    
    return {
        "status": "success",
        "leaked": is_leaked,
        "ai_score": strength_data["score"],
        "entropy": strength_data["entropy"],
        "suggestions": strength_data["suggestion"]
    }
    
