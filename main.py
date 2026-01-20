import requests
import os
import google.generativeai as genai

# --- 1. SETUP ---
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

# KITA GANTI KE 'gemini-pro' (Versi paling stabil & umum)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': pesan, 'parse_mode': 'Markdown'}
    requests.post(url, json=payload)

def ambil_harga():
    try:
        # Ambil harga dari CoinGecko
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        r = requests.get(url, timeout=10)
        return r.json()['bitcoin']['usd']
    except:
        return 0

def analisis_ai(harga):
    prompt = f"""
    Kamu adalah Crypto Analyst. Harga Bitcoin: ${harga:,.2f}.
    Berikan analisis singkat (Bahasa Indonesia):
    1. Tren: (Bullish/Bearish)
    2. Support & Resistance terdekat.
    3. Saran: (Beli/Jual/Tahan)
    
    Jangan terlalu panjang, to the point saja.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"ERROR_AI: {e}"

def main():
    harga = ambil_harga()
    
    if harga == 0:
        kirim_telegram("⚠️ Gagal koneksi ke CoinGecko.")
        return

    analisa = analisis_ai(harga)
    
    # Format Pesan
    if "ERROR_AI" in analisa:
        pesan = f"⚠️ **AI ERROR**\n`{analisa}`"
    else:
        pesan = f"💎 **BTC UPDATE**\nPrice: `${harga:,.2f}`\n\n{analisa}"

    kirim_telegram(pesan)

if __name__ == "__main__":
    main()
