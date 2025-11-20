#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
#  Password Guard - Termux Installer
#  Coded by : Kiran Mondal
#  Repo     : https://github.com/Kiran-mondal/Password-Guard.git
# ============================================================

clear

# ---------------- LOGO ----------------
echo -e "\e[34m"
echo "  ██████  ██    ██ ███████ ██████   █████  ██    ██ ██████  "
echo " ██       ██    ██ ██      ██   ██ ██   ██ ██    ██ ██   ██ "
echo " ██   ███ ██    ██ █████   ██████  ███████ ██    ██ ██   ██ "
echo " ██    ██ ██    ██ ██      ██   ██ ██   ██  ██  ██  ██   ██ "
echo "  ██████   ██████  ███████ ██   ██ ██   ██   ████   ██████  "
echo "              🔐 PASSWORD GUARD (Termux Installer)"
echo -e "\e[0m"
echo "------------------------------------------------------------"
echo "💙 Coded by: Kiran Mondal"
echo "------------------------------------------------------------"

sleep 1

# ---------------- UPDATE & INSTALL DEPENDENCIES ----------------
echo "🔄 Updating Termux..."
pkg update -y && pkg upgrade -y

echo "📦 Installing dependencies..."
pkg install -y python git wget openssl clang make libffi

echo "📦 Installing Python modules..."
pip install --upgrade pip
pip install requests rich beautifulsoup4 sqlite3 speechrecognition pyaudio

# ---------------- CLONE OR UPDATE REPO ----------------
APP_DIR=$HOME/Password-Guard

if [ -d "$APP_DIR" ]; then
    echo "🔁 Existing installation found. Updating..."
    cd "$APP_DIR" && git pull
else
    echo "⬇️  Cloning Password Guard..."
    git clone https://github.com/Kiran-mondal/Password-Guard.git $APP_DIR
    cd "$APP_DIR"
fi

# ---------------- ASK DB MODE ----------------
echo ""
echo "🌐 Choose Database Mode (local / cloud / both): "
read dbmode

# save to config file
echo "DB_MODE = '$dbmode'" > config/app_config.py

echo "📌 Database Mode Saved: $dbmode"

# ---------------- BUILD DATABASE ----------------
echo "🛠 Initializing Local DB (if required)..."
python setup.py

# ---------------- CREATE GLOBAL COMMAND (pg) ----------------
echo "⚙️ Creating global command 'pg'..."

cat << EOF > $PREFIX/bin/pg
#!/bin/bash
python3 $APP_DIR/password_guard.py "\$@"
EOF

chmod +x $PREFIX/bin/pg

# ---------------- FINISH ----------------
clear
echo -e "\e[32m"
echo "🎉 Installation Complete!"
echo -e "\e[33mYou can now run Password Guard using:"
echo -e "\e[36m    pg check"
echo "    pg scan"
echo "    pg stats"
echo -e "\e[32m------------------------------------------------------------"
echo -e "\e[34m💙 Coded by: Kiran Mondal"
echo -e "\e[0m------------------------------------------------------------"
