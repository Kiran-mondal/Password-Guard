# api/html_views.py

def get_base_html(title, active_path, content):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} | Password Guard</title>
        <link rel="icon" type="image/svg+xml" href="https://raw.githubusercontent.com/Kiran-mondal/Password-Guard/main/assets/logo.svg">
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="bg-glow glow-1"></div>
        <div class="bg-glow glow-2"></div>

        <div class="tech-graphics">
            <div class="circle-outer"></div>
            <div class="circle-inner"></div>
            <div class="core-eye"></div>
        </div>

        <nav>
            <div class="logo scramble-text" data-value="PASSWORD GUARD" style="color:var(--accent-cyan); font-weight: bold; font-size: 1.2rem; cursor: pointer;" onclick="window.location.href='/'">PASSWORD GUARD</div>
            <div class="hamburger" onclick="toggleMobileMenu()">≡</div>
            
            <ul class="nav-links" id="navLinks">
                <li><a href="/" class="{'active-link' if active_path == '/' else 'nav-item'}">Home</a></li>
                <li><a href="/about" class="{'active-link' if active_path == '/about' else 'nav-item'}">About</a></li>
                <li><a href="/cli" class="{'active-link' if active_path == '/cli' else 'nav-item'}">CLI Setup</a></li>
                <li><a href="/github" class="{'active-link' if active_path == '/github' else 'nav-item'}">My Projects</a></li>
            </ul>
        </nav>

        {content}

        <script>
            function toggleMobileMenu() {{
                const navLinks = document.getElementById("navLinks");
                navLinks.classList.toggle("active");
            }}

            const scrambleCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+~`|}}{{[]:;?><,./-=";

            document.addEventListener('DOMContentLoaded', initScramble);

            function initScramble() {{
                document.querySelectorAll('.scramble-text').forEach(element => {{
                    element.addEventListener('mouseover', event => {{
                        runScrambleEffect(event.target);
                    }});
                    runScrambleEffect(element); 
                    setInterval(() => {{
                        runScrambleEffect(element);
                    }}, 15000);
                }});
            }}

            function runScrambleEffect(element) {{
                let iterations = 0;
                const originalText = element.dataset.value;
                
                clearInterval(element.interval);
                
                element.interval = setInterval(() => {{
                    element.innerText = originalText
                    .split("")
                    .map((letter, index) => {{
                        if (letter === " ") return " ";
                        if (index < iterations) {{
                            return originalText[index];
                        }}
                        return scrambleCharacters[Math.floor(Math.random() * scrambleCharacters.length)];
                    }})
                    .join("");
                    
                    if (iterations >= originalText.length) {{
                        clearInterval(element.interval);
                    }}
                    iterations += 1 / 3; 
                }}, 30); 
            }}

            function toggleMask() {{
                const input = document.getElementById("pwdInput");
                if(!input) return;
                const toggle = document.getElementById("maskToggle");
                input.type = toggle.checked ? "password" : "text";
            }}

            function evaluateRealtime() {{
                const inputElement = document.getElementById("pwdInput");
                if(!inputElement) return;
                const pwd = inputElement.value;
                
                const rLen = pwd.length >= 8;
                const rUp = /[A-Z]/.test(pwd);
                const rLow = /[a-z]/.test(pwd);
                const rNum = /[0-9]/.test(pwd);
                const rSpc = /[!@#$%^&*()_+\-=\\[\\]{{}};':"\\\\|,.<>\\/?]/.test(pwd);

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
                
                if (score === 0) {{
                    fill.style.backgroundColor = "transparent";
                    text.innerText = "Strength: None";
                    fStr.innerText = "None";
                }} else if (score <= 40) {{
                    fill.style.backgroundColor = "var(--danger)";
                    text.innerText = "Strength: Weak";
                    fStr.innerText = "Weak";
                }} else if (score <= 75) {{
                    fill.style.backgroundColor = "var(--warning)";
                    text.innerText = "Strength: Good";
                    fStr.innerText = "Good";
                }} else {{
                    fill.style.backgroundColor = "var(--success)";
                    text.innerText = "Strength: Strong";
                    fStr.innerText = "Strong";
                }}

                let pool = 0;
                if(rLow) pool += 26;
                if(rUp) pool += 26;
                if(rNum) pool += 10;
                if(rSpc) pool += 33;
                let entropy = pool === 0 ? 0 : Math.round(Math.log2(Math.pow(pool, pwd.length)));
                
                document.getElementById("entropyText").innerText = entropy + " bits entropy";
                document.getElementById("finalEntropy").innerText = entropy + " bits";
            }}

            function generatePassword() {{
                const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+";
                let password = "";
                for (let i = 0; i < 12; i++) {{
                    password += chars.charAt(Math.floor(Math.random() * chars.length));
                }}
                const input = document.getElementById("pwdInput");
                if(input) {{
                    document.getElementById("maskToggle").checked = false;
                    toggleMask();
                    input.value = password;
                    evaluateRealtime(); 
                }}
            }}

            async function checkCloudBreach() {{
                const inputElement = document.getElementById("pwdInput");
                if(!inputElement) return;
                const pwd = inputElement.value;
                const resultBox = document.getElementById("resultBox");
                if(!pwd) {{ alert("Please enter a password!"); return; }}

                resultBox.style.display = "block";
                resultBox.style.backgroundColor = "#1e293b";
                resultBox.innerHTML = "Scanning Neon Cloud Database... ⏳";

                try {{
                    const response = await fetch("/api/scan", {{
                        method: "POST",
                        headers: {{ "Content-Type": "application/json" }},
                        body: JSON.stringify({{ password: pwd }})
                    }});
                    
                    const data = await response.json();
                    
                    if(data.leaked) {{
                        resultBox.style.backgroundColor = "#991b1b";
                        resultBox.innerHTML = `🚨 <b>CRITICAL ALERT:</b> Password found in leaks!<br><br><b>AI Score:</b> ${{data.ai_score}}/100<br><b>Tips:</b> ${{data.suggestions.join(', ')}}`;
                    }} else if(data.ai_score < 70) {{
                        resultBox.style.backgroundColor = "#b45309";
                        resultBox.innerHTML = `⚠️ <b>Safe, but Weak.</b><br><br><b>AI Score:</b> ${{data.ai_score}}/100<br><b>Tips:</b> ${{data.suggestions.join(', ')}}`;
                    }} else {{
                        resultBox.style.backgroundColor = "#166534";
                        resultBox.innerHTML = `✅ <b>Safe & Strong!</b><br><br><b>AI Score:</b> ${{data.ai_score}}/100<br>No leaks found.`;
                    }}
                }} catch(err) {{
                    resultBox.innerHTML = "❌ Error connecting to secure server.";
                }}
            }}

            function showInstallGuide(os) {{
                const installCmds = {{
                    linux: "curl -sO https://raw.githubusercontent.com/Kiran-mondal/Password-Guard/main/installers/install_linux.sh && bash install_linux.sh",
                    termux: "curl -sO https://raw.githubusercontent.com/Kiran-mondal/Password-Guard/main/installers/install_termux.sh && bash install_termux.sh",
                    windows: "git clone https://github.com/Kiran-mondal/Password-Guard.git\\ncd Password-Guard\\npip install -r requirements.txt"
                }};
                const osTitles = {{ linux: "🐧 Linux Terminal", termux: "📱 Termux (Android)", windows: "🪟 Windows CMD" }};
                
                const guide = document.getElementById("cliGuide");
                if(guide) {{
                    document.getElementById("osTitle").innerText = osTitles[os];
                    document.getElementById("installCommand").innerText = installCmds[os];
                    guide.style.display = "block";
                }}
            }}

            function copyText(elementId) {{
                navigator.clipboard.writeText(document.getElementById(elementId).innerText);
                alert("Copied to clipboard!");
            }}
        </script>
    </body>
    </html>
    """

def get_home_content():
    return """
    <div class="container">
        <div class="hero-text">
            <h1 class="scramble-text" data-value="PASSWORD GUARD">PASSWORD GUARD</h1>
            <p>Advanced AI-powered password protection & vault management tool. Ensure your digital life is secure by checking password strength and detecting breaches instantly without storing your sensitive data.</p>
        </div>

        <div class="scanner-card">
            <h2>Password Strength Scanner</h2>
            <div class="input-group">
                <label for="pwdInput">Active Password Entry:</label>
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
                <div class="stat-box"><h4>Strength</h4><span id="finalStrength">None</span></div>
                <div class="divider"></div>
                <div class="stat-box"><h4>Entropy</h4><span id="finalEntropy">0 bits</span></div>
            </div>
            <div class="controls">
                <span>Password Masking</span>
                <label class="switch">
                    <input type="checkbox" id="maskToggle" aria-label="Toggle Password Masking" checked onchange="toggleMask()">
                    <span class="slider"></span>
                </label>
            </div>
            <button class="btn-action btn-suggest" onclick="generatePassword()">Suggest Strong Password</button>
            <button class="btn-action btn-scan" onclick="checkCloudBreach()">Cloud Breach Scan</button>
            <div id="resultBox"></div>
        </div>
    </div>
    """

def get_about_content():
    return """
    <div class="container" style="justify-content: center; text-align: center; min-height: 70vh;">
        <div class="hero-text" style="padding: 0; max-width: 750px; margin: 0 auto; background: rgba(18, 31, 61, 0.7); padding: 40px; border-radius: 20px; border: 1px solid rgba(0,229,255,0.2); backdrop-filter: blur(10px);">
            <h1 class="scramble-text" data-value="ABOUT PASSWORD GUARD" style="font-size: 2rem; margin-bottom: 20px; font-weight: 500; color: var(--accent-cyan);">ABOUT PASSWORD GUARD</h1>
            <div style="width: 80px; height: 3px; background: var(--accent-cyan); margin: 0 auto 25px auto; box-shadow: 0 0 10px var(--accent-cyan);"></div>
            <p style="font-size: 1rem; margin: 0 auto 20px auto; color: #cbd5e1; line-height: 1.7; text-align: center;">Built with modern web technologies, this tool guarantees your data privacy by performing complex entropy calculations directly in memory without saving plaintext passwords.</p>
            <p style="font-size: 1rem; margin: 0 auto 30px auto; color: #cbd5e1; line-height: 1.7; text-align: center;">Whether you are an everyday user securing your accounts or a cybersecurity enthusiast needing advanced terminal-based vault management, Password Guard provides the ultimate offline and cloud-verified defense system.</p>
            <button class="btn-learn" onclick="window.location.href='/'" style="margin-top: 10px; font-size: 1rem; padding: 10px 30px;">Go to Scanner</button>
        </div>
    </div>
    """

def get_cli_content():
    return """
    <div class="container" style="justify-content: center; min-height: 70vh;">
        <div class="bottom-section" style="width: 100%; max-width: 900px; margin: 0 auto; background: rgba(18, 31, 61, 0.7); border: 1px solid rgba(0,229,255,0.2);">
            <h2 class="scramble-text" data-value="CLI Installation Option" style="font-size: 2rem;">CLI Installation Option</h2>
            <div class="bottom-line"></div>
            <p style="font-size: 1rem; color: #cbd5e1; margin-bottom: 35px;">For maximum privacy and offline vault management, download the command-line interface. Run deep system scans, generate passwords, and manage your encrypted local database securely from your terminal.</p>
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
                    <div id="usageCommand" class="code-block"><span class="comment"># Scan a password</span>\npython main.py --scan "your_password"\n\n<span class="comment"># Generate a strong password</span>\npython main.py --generate\n\n<span class="comment"># Scan device for saved browser passwords</span>\npython main.py --devicescan</div>
                </div>
            </div>
        </div>
    </div>
    """
def get_github_content():
    all_projects = [
        {
            "id": "password-guard",
            "title": "Password Guard",
            "desc": "Advanced AI-powered password protection & vault management tool with 3D Cyber UI.",
            "live": "https://passwordguard.quarry.dpdns.org",
            "code": "https://github.com/Kiran-mondal/Password-Guard",
            "svg": '''<svg width="36" height="36" viewBox="0 0 512 512" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="512" height="512" rx="120" fill="#0D4FF0"/><path d="M256 80L120 140V240C120 330 176 407 256 432C336 407 392 330 392 240V140L256 80Z" fill="white"/><circle cx="256" cy="255" r="70" fill="#0D4FF0"/><rect x="235" y="240" width="42" height="75" rx="8" fill="white"/></svg>'''
        },
        {
            "id": "pachisi",
            "title": "Pachisi",
            "desc": "Play the ancient Indian epic board game of strategy, heritage, and royal culture.",
            "live": "https://pachisi.quarry.dpdns.org",
            "code": "https://github.com/Kiran-mondal",
            "svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="36" height="36"><defs><mask id="pasha-hole"><rect width="512" height="512" fill="white" /><circle cx="256" cy="256" r="32" fill="black" /></mask></defs><g mask="url(#pasha-hole)" fill="#dc2626"><rect x="232" y="16" width="48" height="480" rx="12" /><rect x="232" y="16" width="48" height="480" rx="12" transform="rotate(45 256 256)" /><rect x="232" y="16" width="48" height="480" rx="12" transform="rotate(90 256 256)" /><rect x="232" y="16" width="48" height="480" rx="12" transform="rotate(135 256 256)" /><circle cx="256" cy="256" r="168" fill="none" stroke="#dc2626" stroke-width="48" /><circle cx="256" cy="256" r="56" fill="none" stroke="#dc2626" stroke-width="48" /></g></svg>'''
        },
        {
            "id": "zendrift",
            "title": "ZenDrift",
            "desc": "Dynamic performance tracking system built for an engaging and smooth web experience.",
            "live": "https://zendrift.quarry.dpdns.org",
            "code": "https://github.com/Kiran-mondal",
            "svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="36" height="36"><path d="M 120 390 C 120 270, 392 350, 392 210 C 392 130, 310 90, 256 90" fill="none" stroke="#58a6ff" stroke-width="45" stroke-linecap="round" /><circle cx="256" cy="90" r="45" fill="#58a6ff" /></svg>'''
        },
        {
            "id": "omlang",
            "title": "Omlang",
            "desc": "A modern language and communication-focused platform with an intuitive user interface.",
            "live": "https://omlang.quarry.dpdns.org",
            "code": "https://github.com/Kiran-mondal",
            "svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="36" height="36"><path d="M 280 250 C 420 250, 420 380, 350 400 C 450 420, 450 580, 280 580" stroke="#00f2fe" stroke-width="45" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="450" cy="120" r="30" fill="#00f2fe" /></svg>'''
        },
        {
            "id": "chaturanga",
            "title": "Chaturanga",
            "desc": "Interactive web-based application focused on deep logic, planning, and strategy.",
            "live": "https://chaturanga.quarry.dpdns.org",
            "code": "https://github.com/Kiran-mondal",
            "svg": '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" width="36" height="36"><circle cx="50" cy="50" r="48" fill="#d97706" stroke="#ffffff" stroke-width="2"/><path d="M50 20 L75 55 L50 80 L25 55 Z" fill="#ffffff" /></svg>'''
        }
    ]

    cards_html = ""
    for p in all_projects:
        if p["id"] == "password-guard":
            continue
        cards_html += f"""
            <div class="repo-card">
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 10px;">
                    {p['svg']}
                    <h3 style="margin: 0; font-size: 1.3rem; color: var(--accent-cyan);">{p['title']}</h3>
                </div>
                <p>{p['desc']}</p>
                <div class="repo-links">
                    <a href="{p['live']}" target="_blank">Live App</a>
                    <a href="{p['code']}" target="_blank" class="btn-outline">Source Code</a>
                </div>
            </div>
        """

    return f"""
    <div class="container" style="display: block; min-height: 70vh; padding-top: 20px;">
        <div class="github-profile">
            <img src="https://github.com/Kiran-mondal.png" alt="Kiran Mondal">
            <h2 class="scramble-text" data-value="Kiran Mondal">Kiran Mondal</h2>
            <p>Full-Stack Developer & Cyber Security Enthusiast</p>
            <a href="https://github.com/Kiran-mondal" target="_blank" class="btn-github-main">View Full GitHub Profile</a>
        </div>
        <div style="text-align: center; margin-bottom: 35px; margin-top: 50px;">
            <h3 style="color: white; font-size: 1.6rem; margin: 0;">🌐 My Other Live Projects</h3>
            <div class="bottom-line" style="width: 180px; margin: 15px auto 0 auto;"></div>
        </div>
        <div class="repo-grid">
            {cards_html}
        </div>
        <br><br>
    </div>
    """

def get_sitemap_content():
    return """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   <url>
      <loc>https://passwordguard.quarry.dpdns.org/</loc>
      <lastmod>2026-07-27</lastmod>
      <changefreq>weekly</changefreq>
      <priority>1.0</priority>
   </url>
   <url>
      <loc>https://passwordguard.quarry.dpdns.org/about</loc>
      <lastmod>2026-07-27</lastmod>
      <changefreq>monthly</changefreq>
      <priority>0.8</priority>
   </url>
   <url>
      <loc>https://passwordguard.quarry.dpdns.org/cli</loc>
      <lastmod>2026-07-27</lastmod>
      <changefreq>monthly</changefreq>
      <priority>0.8</priority>
   </url>
   <url>
      <loc>https://passwordguard.quarry.dpdns.org/github</loc>
      <lastmod>2026-07-27</lastmod>
      <changefreq>monthly</changefreq>
      <priority>0.9</priority>
   </url>
</urlset>"""
