import sys
import os
import re 

# Vercel Path Fixer
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import hashlib
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from core.ai_strength import AIStrength
from core.breach_check import breach_check

ai = AIStrength()
app = FastAPI(title="Password Guard Web")

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

class PasswordCheckRequest(BaseModel):
    password: str

@app.get("/", response_class=HTMLResponse)
async def serve_website():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Password Guard | Cyber Security</title>
        <link rel="icon" type="image/svg+xml" href="https://raw.githubusercontent.com/Kiran-mondal/Password-Guard/main/assets/logo.svg">
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="bg-glow glow-1"></div>
        <div class="bg-glow glow-2"></div>

        <!-- Sticky Navbar -->
        <nav>
            <div class="logo" style="color:var(--accent-cyan); font-weight: bold; font-size: 1.2rem;">PASSWORD GUARD</div>
            <div class="hamburger" onclick="toggleMobileMenu()">≡</div>
            
            <ul class="nav-links" id="navLinks">
                <!-- Anchor links updated to match section IDs -->
                <li><a href="#home" onclick="toggleMobileMenu()">Home</a></li>
                <li><a href="#scanner-section" onclick="toggleMobileMenu()">Scanner</a></li>
                <li><a href="#cli-section" onclick="toggleMobileMenu()">CLI Setup</a></li>
                <li><a href="https://github.com/Kiran-mondal/Password-Guard" target="_blank" class="btn-signup">GitHub</a></li>
            </ul>
        </nav>

        <!-- Main Hero Section -->
        <div class="container" id="home">
            <div class="tech-graphics">
                <div class="circle-outer"></div>
                <div class="circle-inner"></div>
                <div class="core-eye"></div>
            </div>

            <!-- Left Text -->
            <div class="hero-text">
                <h1>CYBER SECURITY</h1>
                <p>Advanced AI-powered password protection & vault management tool. Ensure your digital life is secure by checking password strength and detecting breaches instantly without storing your sensitive data.</p>
                <button class="btn-learn" onclick="document.querySelector('#scanner-section').scrollIntoView({behavior: 'smooth'})">Try Scanner</button>
            </div>

            <!-- Right Scanner Card -->
            <div class="scanner-card" id="scanner-section">
                <h2>Password Strength Scanner</h2>
                
                <div class="input-group">
                    <label>Active Password Entry:</label>
                    <input type="password" id="pwdInput" placeholder="Type password..." oninput="evaluateRealtime()">
                </div>

                <div class="strength-header">
                    <span id="strengthText">Strength: None</span>
                    <span id="entropyText" style="color: var(--text-muted); font-weight: normal;">0 bits entropy</span>
                </div>
                <div class="strength-bar">
                    <div class="strength-fill" id="strengthFill"></div>
                </div>

                <div class="requirements-title">Requirements Check</div>
                <ul class="requirements">
                    <li id="req-len">At least 8 characters</li>
                    <li id="req-up">Contains uppercase letters</li>
                    <li id="req-low">Contains lowercase letters</li>
                    <li id="req-num">Contains numbers</li>
                    <li id="req-spc">Contains special characters</li>
                </ul>

                <div class="stats-row">
                    <div class="stat-box">
                        <h4>Strength</h4>
                        <span id="finalStrength">None</span>
                    </div>
                    <div class="divider"></div>
                    <div class="stat-box">
                        <h4>Entropy</h4>
                        <span id="finalEntropy">0 bits</span>
                    </div>
                </div>

                <div class="controls">
                    <span>Password Masking</span>
                    <label class="switch">
                        <input type="checkbox" id="maskToggle" checked onchange="toggleMask()">
                        <span class="slider"></span>
                    </label>
                </div>

                <button class="btn-action btn-suggest" onclick="generatePassword()">Suggest Strong Password</button>
                <button class="btn-action btn-scan" onclick="checkCloudBreach()">Cloud Breach Scan</button>
                
                <div id="resultBox"></div>
            </div>
        </div>

        <!-- Bottom CLI Section -->
        <div class="bottom-section" id="cli-section">
            <h2>CLI Installation Option</h2>
            <div class="bottom-line"></div>
            <p>For maximum privacy and offline vault management, download the command-line interface. Run deep system scans, generate passwords, and manage your encrypted local database securely from your terminal.</p>
            
            <div class="cli-buttons">
                <button class="dl-btn" onclick="showInstallGuide('linux')">🐧 Linux Terminal</button>
                <button class="dl-btn" onclick="showInstallGuide('termux')">📱 Termux (Android)</button>
                <button class="dl-btn" onclick="showInstallGuide('windows')">🪟 Windows CMD</button>
            </div>

            <div id="cliGuide" class="cli-guide">
                <h3 id="osTitle">Installation</h3>
                <div class="code-box-container">
                    <button class="small-copy-btn" onclick="copyText('installCommand')">Copy</button>
                    <div id="installCommand" class="code-block"></div>
                </div>
                <h3>🚀 Usage Commands</h3>
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
        </div>

        <!-- JavaScript Logic -->
        <script>
            // Mobile Menu Toggle
            function toggleMobileMenu() {
                const navLinks = document.getElementById("navLinks");
                navLinks.classList.toggle("active");
            }

            function toggleMask() {
                const input = document.getElementById("pwdInput");
                const toggle = document.getElementById("maskToggle");
                input.type = toggle.checked ? "password" : "text";
            }

            function evaluateRealtime() {
                const pwd = document.getElementById("pwdInput").value;
                
                const rLen = pwd.length >= 8;
                const rUp = /[A-Z]/.test(pwd);
                const rLow = /[a-z]/.test(pwd);
                const rNum = /[0-9]/.test(pwd);
                const rSpc = /[!@#$%^&*()_+\-=\\[\\]{};':"\\\\|,.<>\\/?]/.test(pwd);

                document.getElementById("req-len").className = rLen ? "met" : "";
                document.getElementById("req-up").className = rUp ? "met" : "";
                document.getElementById("req-low").className = rLow ? "met" : "";
                document.getElementById("req-num").className = rNum ? "met" : "";
                document.getElementById("req-spc").className = rSpc ? "met" : "";

                let score = 0;
                if(rLen) score += 25;
                if(rUp) score += 15;
                if(rLow) score += 15;
                if(rNum) score += 20;
                if(rSpc) score += 25;

                const fill = document.getElementById("strengthFill");
                const text = document.getElementById("strengthText");
                const fStr = document.getElementById("finalStrength");
                
                fill.style.width = score + "%";
                
                if (score === 0) {
                    fill.style.backgroundColor = "transparent";
                    text.innerText = "Strength: None";
                    fStr.innerText = "None";
                } else if (score <= 40) {
                    fill.style.backgroundColor = "var(--danger)";
                    text.innerText = "Strength: Weak";
                    fStr.innerText = "Weak";
                } else if (score <= 75) {
                    fill.style.backgroundColor = "var(--warning)";
                    text.innerText = "Strength: Good";
                    fStr.innerText = "Good";
                } else {
                    fill.style.backgroundColor = "var(--success)";
                    text.innerText = "Strength: Strong";
                    fStr.innerText = "Strong";
                }

                let pool = 0;
                if(rLow) pool += 26;
                if(rUp) pool += 26;
                if(rNum) pool += 10;
                if(rSpc) pool += 33;
                let entropy = pool === 0 ? 0 : Math.round(Math.log2(Math.pow(pool, pwd.length)));
                
                document.getElementById("entropyText").innerText = entropy + " bits entropy";
                document.getElementById("finalEntropy").innerText = entropy + " bits";
            }

            function generatePassword() {
                const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+";
                let password = "";
                for (let i = 0; i < 12; i++) {
                    password += chars.charAt(Math.floor(Math.random() * chars.length));
                }
                const input = document.getElementById("pwdInput");
                document.getElementById("maskToggle").checked = false;
                toggleMask();
                input.value = password;
                evaluateRealtime(); 
            }

            async function checkCloudBreach() {
                const pwd = document.getElementById("pwdInput").value;
                const resultBox = document.getElementById("resultBox");
                if(!pwd) { alert("Please enter a password!"); return; }

                resultBox.style.display = "block";
                resultBox.style.backgroundColor = "#1e293b";
                resultBox.innerHTML = "Scanning Neon Cloud Database... ⏳";

                try {
                    const response = await fetch("/api/scan", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ password: pwd })
                    });
                    
                    const data = await response.json();
                    
                    if(data.leaked) {
                        resultBox.style.backgroundColor = "#991b1b";
                        resultBox.innerHTML = `🚨 <b>CRITICAL ALERT:</b> Password found in leaks!<br><br><b>AI Score:</b> ${data.ai_score}/100<br><b>Tips:</b> ${data.suggestions.join(', ')}`;
                    } else if(data.ai_score < 70) {
                        resultBox.style.backgroundColor = "#b45309";
                        resultBox.innerHTML = `⚠️ <b>Safe, but Weak.</b><br><br><b>AI Score:</b> ${data.ai_score}/100<br><b>Tips:</b> ${data.suggestions.join(', ')}`;
                    } else {
                        resultBox.style.backgroundColor = "#166534";
                        resultBox.innerHTML = `✅ <b>Safe & Strong!</b><br><br><b>AI Score:</b> ${data.ai_score}/100<br>No leaks found.`;
                    }
                } catch(err) {
                    resultBox.innerHTML = "❌ Error connecting to secure server.";
                }
            }

            const installCmds = {
                linux: "curl -sO https://raw.githubusercontent.com/Kiran-mondal/Password-Guard/main/installers/install_linux.sh && bash install_linux.sh",
                termux: "curl -sO https://raw.githubusercontent.com/Kiran-mondal/Password-Guard/main/installers/install_termux.sh && bash install_termux.sh",
                windows: "git clone https://github.com/Kiran-mondal/Password-Guard.git\\ncd Password-Guard\\npip install -r requirements.txt"
            };
            const osTitles = { linux: "🐧 Linux Terminal", termux: "📱 Termux (Android)", windows: "🪟 Windows CMD" };

            function showInstallGuide(os) {
                const guide = document.getElementById("cliGuide");
                document.getElementById("osTitle").innerText = osTitles[os];
                document.getElementById("installCommand").innerText = installCmds[os];
                guide.style.display = "block";
                setTimeout(() => { 
                    // Adjusted scroll calculation to account for the sticky navbar height
                    const y = guide.getBoundingClientRect().top + window.scrollY - 100;
                    window.scrollTo({top: y, behavior: 'smooth'});
                }, 100);
            }

            function copyText(elementId) {
                navigator.clipboard.writeText(document.getElementById(elementId).innerText);
                alert("Copied to clipboard!");
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/scan")
async def scan_password(req: PasswordCheckRequest):
    pwd = req.password
    
    strength_data = ai.analyze(pwd)
    is_leaked = breach_check(pwd)
    
    has_upper = bool(re.search(r'[A-Z]', pwd))
    has_lower = bool(re.search(r'[a-z]', pwd))
    has_num = bool(re.search(r'[0-9]', pwd))
    has_special = bool(re.search(r'[^A-Za-z0-9]', pwd))
    
    if len(pwd) >= 8 and has_upper and has_lower and has_num and has_special:
        strength_data["score"] = 100
        strength_data["suggestion"] = ["Excellent! Your password meets all standard security criteria."]
    
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
    
