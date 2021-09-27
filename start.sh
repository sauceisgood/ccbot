echo "Cloning Repo..."
git clone https://github.com/sauceisgood/ccbot.git /ccbot
cd /VC_PLAYER
pip3 install -U -r requirements.txt
echo "Starting Bot..."
python3 bot.py
