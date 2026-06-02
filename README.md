# 🔐 Password Guard

> **Secure. Smart. Cloud-Ready.**  
> An advanced AI-powered password protection & vault management tool.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform Support](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20Termux-brightgreen)](https://github.com/Kiran-mondal/Password-Guard)

---

## 🌟 Overview

Password Guard is a **next-generation password manager** designed for developers, professionals, and everyday users who demand **military-grade security** without compromising on usability. 

Your passwords stay with you — not with us. 🔒

### Why Password Guard?

- ✅ **AI-Powered Security** - Get intelligent password strength ratings and recommendations
- ✅ **Zero-Knowledge Architecture** - Your vault is encrypted locally; we never see your data
- ✅ **Multi-Platform** - Works seamlessly on Linux, Windows, Termux, and more
- ✅ **Multi-Language Support** - English, Bengali, Hindi (with more languages coming)
- ✅ **Real-Time Alerts** - Get notified of password breaches and security risks instantly
- ✅ **Optional Cloud Sync** - Securely sync your vault across all your devices

---

## ⚡ Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

**Clone the Repository:**
```bash
git clone https://github.com/Kiran-mondal/Password-Guard.git
cd Password-Guard
```

**Install Dependencies:**
```bash
pip install -r requirements.txt --use-feature=fast-deps
```

**Run the Application:**
```bash
python main.py
```

### Platform-Specific Instructions

#### 🐧 Linux / Termux
```bash
# Install system dependencies (if needed)
sudo apt-get update
sudo apt-get install python3-pip python3-dev

# Follow the Quick Start steps above
git clone https://github.com/Kiran-mondal/Password-Guard.git
cd Password-Guard
pip install -r requirements.txt --use-feature=fast-deps
python main.py
```

#### 🪟 Windows
```bash
# Using Command Prompt or PowerShell
git clone https://github.com/Kiran-mondal/Password-Guard.git
cd Password-Guard
pip install -r requirements.txt --use-feature=fast-deps
python main.py
```

---

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI Security Rating** | Get intelligent password strength scores with actionable suggestions for improvement |
| 📊 **Analytics Dashboard** | View comprehensive stats on password strength, breach risks, and reuse patterns |
| ☁️ **Cloud Sync (Optional)** | Securely sync your encrypted vault across multiple devices |
| 🚨 **Real-Time Alerts** | Receive instant notifications about password breaches and security threats |
| 🔐 **Military-Grade Encryption** | AES encryption + Hashing for maximum security |
| 🎭 **Multi-Language Support** | English 🇬🇧 • বাংলা 🇧🇩 • हिन्दी 🇮🇳 |
| 🔑 **Auto-Generate Passwords** | Create strong, random passwords with custom rules |
| 🏠 **Local Vault Storage** | SQLite-based local storage (optional cloud backup) |

---

## 🛠️ Tech Stack

- **Backend:** Python 3.8+
- **Database:** SQLite (Local) / Cloud DB (Optional)
- **Encryption:** AES-256 + SHA-256 Hashing
- **AI/ML:** Password strength analysis model
- **UI:** Command-line interface with multi-language support

---

## 🌐 Supported Languages

| Language | Code | Status |
|----------|------|--------|
| English | `en` | ✅ Default |
| বাংলা (Bengali) | `bn` | ✅ Supported |
| हिन्दी (Hindi) | `hi` | ✅ Supported |

**Want to add more languages?** Check our [Contributing Guide](#-contribute)

---

## 📚 Usage

### Basic Operations

**Create a New Password:**
```
1. Launch Password Guard
2. Select "Add Password"
3. Enter website/service name, username, and password
4. AI will rate your password strength
5. Password is encrypted and saved locally
```

**View Password Statistics:**
```
1. Go to "Dashboard"
2. Check password strength distribution
3. Review potential security issues
4. Get recommendations for weak passwords
```

**Enable Cloud Sync:**
```
1. Navigate to "Settings"
2. Select "Enable Cloud Sync"
3. Authenticate with your secure cloud account
4. Your vault will sync automatically
```

---

## 🔒 Security & Privacy

Password Guard follows security best practices:

- ✅ **End-to-End Encryption** - All data encrypted with AES-256
- ✅ **No Telemetry** - We don't collect or send your data
- ✅ **Open Source** - Code is publicly auditable
- ✅ **Local-First** - Vault stored locally by default
- ✅ **Optional Cloud** - You control what syncs to the cloud
- ✅ **MIT License** - Free to use, modify, and distribute

---

## 🚀 Roadmap

- 🔲 **Browser Extension** - Autofill support for Chrome, Firefox, Safari
- 🔲 **Biometric Unlock** - Facial recognition & fingerprint authentication
- 🔲 **Advanced 2FA** - OTP + Hardware security key support
- 🔲 **Team/Enterprise Plan** - Shared vaults and admin dashboard
- 🔲 **Mobile App** - Native iOS & Android applications
- 🔲 **Dark Mode** - Enhanced UI themes
- 🔲 **Password Audit** - Automated security scanning

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named..."
**Solution:** Reinstall dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Application won't start on Windows
**Solution:** Use Python 3.8+ and ensure pip is updated
```bash
python --version
pip install --upgrade pip
```

### Permission Denied on Linux/Termux
**Solution:** Ensure proper permissions
```bash
chmod +x main.py
python main.py
```

### Cloud Sync not working
**Solution:** Check internet connection and cloud credentials in Settings

---

## 📦 Project Structure

```
Password-Guard/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── config/
│   ├── settings.json      # Configuration & preferences
│   └── languages/         # Multi-language files (en, bn, hi)
├── src/
│   ├── vault.py          # Vault management core
│   ├── encryption.py     # AES encryption module
│   ├── ai_security.py    # AI password strength analyzer
│   └── cloud_sync.py     # Cloud synchronization
├── ui/
│   └── cli.py            # Command-line interface
└── README.md             # This file
```

---

## 🧑‍💻 Contributing

We welcome contributions from developers of all levels! 

### Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/Password-Guard.git
   cd Password-Guard
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Write clean, documented code
   - Follow PEP 8 style guidelines
   - Add comments for complex logic

4. **Test Your Changes**
   ```bash
   python -m pytest tests/
   ```

5. **Commit & Push**
   ```bash
   git add .
   git commit -m "Add: Brief description of your feature"
   git push origin feature/your-feature-name
   ```

6. **Submit a Pull Request**
   - Describe your changes clearly
   - Reference any related issues
   - Include screenshots/examples if applicable

### Areas We Need Help With

- 🌍 **Translations** - Help translate to more languages
- 🧪 **Testing** - Write unit and integration tests
- 📚 **Documentation** - Improve guides and examples
- 🐛 **Bug Fixes** - Report and fix issues
- ✨ **Features** - Implement roadmap items

### Code Guidelines

- Use meaningful variable names
- Add docstrings to functions
- Keep functions small and focused
- Write tests for new features
- Update documentation

---

## 📄 License

This project is licensed under the **MIT License** — you are free to use, modify, distribute, and use privately, as long as you include the original license and copyright notice.

See [LICENSE](LICENSE) for details.

---

## ⭐ Show Your Support

If Password Guard helps you manage your digital security better, please:

1. **Star ⭐ this repository** on GitHub
2. **Share it** with your network
3. **Contribute** code, translations, or ideas
4. **Report bugs** to help us improve

Your support motivates ongoing development and helps us bring cloud release closer! 🚀

---

## 📞 Support & Feedback

- 🐛 **Report Issues:** [GitHub Issues](https://github.com/Kiran-mondal/Password-Guard/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/Kiran-mondal/Password-Guard/discussions)
- 📧 **Contact:** Open an issue or PR with your questions

---

## 🙏 Acknowledgments

- Built with ❤️ for security-conscious developers
- Inspired by open-source password management principles
- Thanks to all contributors and users

---

## 📝 Changelog

### v1.0.0 (Initial Release)
- ✅ AI-powered password strength rating
- ✅ Multi-language support (EN, BN, HI)
- ✅ Local vault encryption
- ✅ Dashboard analytics
- ✅ Auto-alert system

---

<div align="center">

### 🔐 Your Digital Keys Protected by Intelligence

**[Star the repo](https://github.com/Kiran-mondal/Password-Guard) • [Report a Bug](https://github.com/Kiran-mondal/Password-Guard/issues) • [Suggest a Feature](https://github.com/Kiran-mondal/Password-Guard/issues)**

Made with 💙 by [Kiran Mondal](https://github.com/Kiran-mondal)

</div>