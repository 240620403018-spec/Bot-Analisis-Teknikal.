import requests
import os
import google.generativeai as genai
import time

# --- 1. SETUP ---
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

genai.configure(api_key=GEMINI_API_KEY)

# DAFTAR MODEL (Sistem Anti-Mogok)
DAFTAR_MODEL = [
    'gemini-2.0-flash-lite-preview-02-05', # Kuda hitam (Cepat & Hemat)
    'gemini-flash-latest',                 # Stabil
    'gemini-2.0-flash-exp',                # Canggih (Experimental)
    'gemini-1.5-flash'                     # Cadangan terakhir
]

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': pesan, 'parse_mode': 'Markdown'}
    requests.post(url, json=payload)

def ambil_data_market():
    try:
        # Kita ambil BTC dan SOL sekaligus
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,solana&vs_currencies=usd"
        r = requests.get(url, timeout=10)
        data = r.json()
        btc = data['bitcoin']['usd']
        sol = data['solana']['usd']
        return btc, sol
    except:
        return 0, 0

def analisis_market(btc, sol):
    prompt = f"""
    Kamu adalah Senior Crypto Strategist.
    DATA PASAR SAAT INI:
    - Bitcoin (BTC): ${btc:,.2f}
    - Solana (SOL): ${sol:,.2f}
    
    Tugas: Analisis potensi SOLANA berdasarkan pergerakan BTC.
    Jawab singkat padat (Bahasa Indonesia):
    
    1. 🔗 **Korelasi**: (Apakah BTC menyeret SOL naik/turun? Jelaskan dalam 1 kalimat)
    2. 🚦 **Sinyal SOL**: (BULLISH / BEARISH / WAIT)
    3. 🎯 **Level Kunci SOL**: (Tentukan Support & Resistance terdekat)
    4. 💡 **Saran Action**: (Serok Bawah / TP / Wait)
    """
    
    # --- LOGIKA AUTO-SWITCHING ---
    for nama_model in DAFTAR_MODEL:
        try:
            model = genai.GenerativeModel(nama_model)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gagal {nama_model}, ganti mesin...")
            time.sleep(1)
            
    return "SEMUA_MODEL_SIBUK"

def main():
    btc, sol = ambil_data_market()
    
    if btc == 0:
        kirim_telegram("⚠️ Gagal koneksi ke CoinGecko.")
        return

    hasil_analisis = analisis_market(btc, sol)
    
    if hasil_analisis == "SEMUA_MODEL_SIBUK":
        pesan = "⚠️ **SERVER SIBUK**\nGoogle AI sedang penuh. Coba 15 menit lagi."
    else:
        # Format Laporan Keren
        pesan = f"""
🔥 **MARKET DUO UPDATE**
---------------------------
👑 **BTC**: `${btc:,.2f}`
⚡ **SOL**: `${sol:,.2f}`

{hasil_analisis}
        """

    kirim_telegram(pesan)

if __name__ == "__main__":
    main()
