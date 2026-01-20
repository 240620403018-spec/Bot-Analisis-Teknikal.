import requests
import os
import google.generativeai as genai
import time

# --- 1. SETUP ---
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

genai.configure(api_key=GEMINI_API_KEY)

# --- DAFTAR MODEL YANG AKAN DICOBA (BERURUTAN) ---
# Kita pakai model 'Lite' dan 'Latest' yang biasanya lebih longgar kuotanya
DAFTAR_MODEL = [
    'gemini-2.0-flash-lite-preview-02-05', # Coba versi Lite dulu (Biasanya lancar)
    'gemini-flash-latest',                 # Cadangan 1 (Versi Stabil)
    'gemini-2.0-flash-exp',                # Cadangan 2 (Versi Eksperimental)
    'gemini-1.5-flash'                     # Cadangan 3 (Versi Lama)
]

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': pesan, 'parse_mode': 'Markdown'}
    requests.post(url, json=payload)

def ambil_harga():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        r = requests.get(url, timeout=10)
        return r.json()['bitcoin']['usd']
    except:
        return 0

def analisis_pintar(harga):
    prompt = f"""
    Kamu adalah Crypto Strategist. Harga BTC: ${harga:,.2f}.
    Berikan sinyal trading super singkat (Bahasa Indonesia):
    1. 🚦 Sinyal: (BULLISH/BEARISH/NEUTRAL)
    2. 🎯 Target: (Support & Resistance)
    3. 📢 Action: (Buy Dip / Hold / Sell)
    """
    
    # --- LOGIKA AUTO-SWITCHING ---
    laporan_error = []
    
    for nama_model in DAFTAR_MODEL:
        try:
            # Coba model satu per satu
            model = genai.GenerativeModel(nama_model)
            response = model.generate_content(prompt)
            return response.text # Kalau berhasil, langsung kembali
        except Exception as e:
            # Kalau gagal, catat errornya dan lanjut ke model berikutnya
            print(f"Gagal pakai {nama_model}: {e}")
            laporan_error.append(f"{nama_model}: {e}")
            time.sleep(1) # Istirahat 1 detik sebelum coba lagi
            
    # Kalau semua model gagal, baru nyerah
    return "SEMUA_MODEL_GAGAL"

def main():
    harga = ambil_harga()
    if harga == 0:
        kirim_telegram("⚠️ Gagal koneksi data harga.")
        return

    hasil = analisis_pintar(harga)
    
    if hasil == "SEMUA_MODEL_GAGAL":
        pesan = "⚠️ **BOT SEDANG SIBUK**\nSemua server AI sedang penuh/limit. Coba lagi 15 menit lagi."
    else:
        pesan = f"⚡ **BTC FLASH UPDATE**\nPrice: `${harga:,.2f}`\n\n{hasil}"

    kirim_telegram(pesan)

if __name__ == "__main__":
    main()
