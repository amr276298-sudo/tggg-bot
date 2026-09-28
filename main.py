import os, requests, telebot, threading
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def get_price():
    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/TQQQ?interval=1d&range=2d"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).json()
        m = r['chart']['result'][0]['meta']
        p = m['regularMarketPrice']
        prev = m['chartPreviousClose']
        return p, p-prev, (p-prev)/prev*100
    except:
        return None, None, None

@bot.message_handler(commands=['start','price','tqqq'])
def h(m):
    p,c,pct = get_price()
    if p:
        e="🟢" if c>=0 else "🔴"
        bot.reply_to(m, f"{e} TQQQ: ${p:.2f}\n{c:+.2f} ({pct:+.2f}%)")
    else:
        bot.reply_to(m, "حاول مرة ثانية")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()
