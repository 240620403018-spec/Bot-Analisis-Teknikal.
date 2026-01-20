import requests
import os
import google.generativeai as genai
import time

# --- 1. SETUP ---
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

# Kita coba pakai model yang paling umum (gemini-pro) agar lebih stabil
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': pesan, 'parse_mode': 'Markdown'}
    requests.post(url, json=payload)

def ambil_harga():
    # Gunakan CoinGecko (Stabil)
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        r = requests.get(url, timeout=10)
        return r.json()['bitcoin']['usd']
    except:
        return 0 # Gagal ambil harga

def analisis_ai(harga):
    # INI PROMPT AGAR GAYA BICARA SEPERTI SAYA (ANALYST)
    prompt = f"""
    Bertindaklah sebagai Senior Crypto Analyst. Harga Bitcoin sekarang: ${harga:,.2f}.
    
    Berikan analisis teknikal singkat (poin-poin) dalam Bahasa Indonesia:
    1. 🐂/🐻 Bias: (Bullish/Bearish/Neutral)
    2. 🧱 Key Level: (Perkirakan Support & Resistance terdekat dari angka psikologis harga tersebut)
    3. 💡 Saran Action: (Wait and See / DCA / Take Profit)
    
    Jawab dengan tegas, singkat, dan profesional tanpa basa-basi.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # PENTING: Jika error, kita kirim pesan error aslinya agar ketahuan
        return f"ERROR_AI: {e}"

def main():
    harga = ambil_harga()
    
    if harga == 0:
        kirim_telegram("⚠️ Gagal mengambil data harga dari CoinGecko.")
        return

    analisa = analisis_ai(harga)
    
    # Cek apakah AI Error atau Sukses
    if "ERROR_AI" in analisa:
        # Kirim pesan error ke Telegram
        pesan = f"⚠️ **AI GAGAL MERESPON**\n\nPenyebab: `{analisa}`\n\n*Solusi: Cek GEMINI_API_KEY di GitHub Secrets Anda.*"
    else:
        # Kirim Analisis Keren
        pesan = f"💎 **BTC MARKET UPDATE**\nPrice: `${harga:,.2f}`\n\n{analisa}"

    kirim_telegram(pesan)

if __name__ == "__main__":
    main()
