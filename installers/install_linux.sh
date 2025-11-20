#!/usr/bin/env bash
# ============================================================
#  Password Guard - Linux Installer
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
echo "              🔐 PASSWORD GUARD (Linux Installer)"
echo -e "\e[0m"
echo "------------------------------------------------------------"
echo "💙 Coded by: Kiran Mondal"
echo "------------------------------------------------------------"

sleep 1

# ---------------- UPDATE & INSTALL DEPENDENCIES ----------------
echo "🔄 Updating system..."
sudo apt update -y && sudo apt upgrade -y

echo "📦 Installing dependencies..."
sudo apt install -y python3 python3-pip python3-dev git build-essential \
                    libssl-dev libffi-dev portaudio19-dev

echo "📦 Installing Python modules..."
pip3 install --upgrade pip
pip3 install requests rich beautifulsoup4 sqlite3 speechrecognition pyaudio

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
echo -e "\e[33m🌐 Choose Database Mode (local / cloud / both): \e[0m"
read dbmode

# save to config file
echo "DB_MODE = '$dbmode'" > config/app_config.py
echo "📌 Database Mode Saved: $dbmode"

# ---------------- BUILD DATABASE ----------------
echo "🛠 Initializing Local DB (if required)..."
python3 setup.py

# ---------------- CREATE GLOBAL COMMAND (pg) ----------------
echo "⚙️ Creating global command 'pg'..."

sudo bash -c "cat << EOF > /usr/local/bin/pg
#!/bin/bash
python3 $APP_DIR/password_guard.py \"\$@\"
EOF"
sudo chmod +x /usr/local/bin/pg

# ---------------- FINISH ----------------
clear
echo -e "\e[32m"
echo "🎉 Installation Complete on Linux!"
echo -e "\e[33mYou can now run Password Guard using:"
echo -e "\e[36m    pg check"
echo "    pg scan"
echo "    pg stats"
echo -e "\e[32m------------------------------------------------------------"
echo -e "\e[34m💙 Coded by: Kiran Mondal"
echo -e "\e[0m------------------------------------------------------------"
