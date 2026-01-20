import requests
import os
import google.generativeai as genai
import time

# --- 1. SETUP ---
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

# KITA GANTI KE VERSI 'EXP' (GRATIS)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': pesan, 'parse_mode': 'Markdown'}
    requests.post(url, json=payload)

def ambil_harga():
    try:
        # Ambil harga Bitcoin dari CoinGecko
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        r = requests.get(url, timeout=10)
        return r.json()['bitcoin']['usd']
    except:
        return 0

def analisis_ai(harga):
    prompt = f"""
    Kamu adalah Crypto Strategist. Harga BTC sekarang: ${harga:,.2f}.
    
    Berikan sinyal trading singkat (Bahasa Indonesia):
    1. 🚦 Sinyal: (BULLISH / BEARISH / NEUTRAL)
    2. 🛡️ Support & Resistance kuncian.
    3. 📢 Saran: (Serok / Tahan / Jual Sebagian)
    
    Gunakan emoji. Jangan bertele-tele.
    """
    try:
        # Tambahkan delay sedikit biar aman
        time.sleep(1) 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"ERROR_AI: {e}"

def main():
    harga = ambil_harga()
    
    if harga == 0:
        kirim_telegram("⚠️ Gagal koneksi data harga.")
        return

    analisa = analisis_ai(harga)
    
    if "ERROR_AI" in analisa:
        # Jika versi EXP pun gagal, kita kasih pesan fallback yang jelas
        if "429" in analisa:
            pesan = "⚠️ **KUOTA HABIS**\nGoogle sedang membatasi akun gratisan. Coba lagi nanti."
        else:
            pesan = f"⚠️ **AI ERROR**\n`{analisa}`"
    else:
        pesan = f"⚡ **BTC FLASH UPDATE**\nPrice: `${harga:,.2f}`\n\n{analisa}"

    kirim_telegram(pesan)

if __name__ == "__main__":
    main()
