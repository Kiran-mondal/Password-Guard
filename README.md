<div align="center">
  <img src="assets/logo.svg" alt="Password Guard Logo" width="150" />
  
  <h1>Password Guard</h1>

  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</div>

<br>

**Password Guard** is an advanced AI-powered password protection & vault management tool. Ensure your digital life is secure by checking password strength and detecting breaches instantly—without ever storing your sensitive data on public servers. Available as both a **Cloud Web Scanner** and an **Offline CLI Tool**.

🌐 **Live Web Version:** [Visit Password Guard Web](https://password-guard-ivory.vercel.app)
---

## ✨ Key Features

- **🤖 AI Strength Analysis:** Calculates entropy, detects predictable patterns, and suggests improvements.
- **🚨 Cloud Breach Scan:** Checks if your password has been compromised in known data breaches.
- **💻 Offline CLI App:** Run deep system scans securely from your terminal.
- **📱 Device Scanner:** Scans your local device for saved browser/app passwords (Requires OS permissions).
- **🪄 Random Password Generator:** Instantly generates mathematically secure 16-character passwords.
- **🎨 Dark Sci-Fi UI:** Beautiful glassmorphism and neon-cyberpunk web interface.

---

## 🚀 Installation (CLI Tool)

For maximum privacy and offline vault management, download the command-line interface.

### 🐧 Linux Terminal
```bash
curl -sO [https://raw.githubusercontent.com/Kiran-mondal/Password-Guard/main/installers/install_linux.sh](https://raw.githubusercontent.com/Kiran-mondal/Password-Guard/main/installers/install_linux.sh) && bash install_linux.sh

```
### 📱 Termux (Android)
```bash
curl -sO [https://raw.githubusercontent.com/Kiran-mondal/Password-Guard/main/installers/install_termux.sh](https://raw.githubusercontent.com/Kiran-mondal/Password-Guard/main/installers/install_termux.sh) && bash install_termux.sh

```
### 🪟 Windows CMD / PowerShell
```cmd
git clone [https://github.com/Kiran-mondal/Password-Guard.git](https://github.com/Kiran-mondal/Password-Guard.git)
cd Password-Guard
pip install -r requirements.txt

```
## 💻 CLI Usage Commands
Once installed, you can use the tool completely offline using the following commands:
**1. Scan a specific password securely:**
```bash
python main.py --scan "your_password_here"

```
**2. Generate a strong, random password:**
```bash
python main.py --generate

```
**3. Scan your device for saved browser passwords:**
```bash
python main.py --devicescan

```
## 🛠️ Tech Stack
 * **Backend / CLI:** Python, FastAPI, SQLite
 * **Frontend (Web):** HTML5, CSS3 (Glassmorphism), Vanilla JavaScript
 * **Cloud Database:** Neon (Serverless Postgres)
 * **Deployment:** Vercel (Web API), GitHub Actions (App Builds)
## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
## 📝 License
This project is MIT licensed.
*Built with ❤️ for Cyber Security.*
