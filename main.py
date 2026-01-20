import requests
import os
import google.generativeai as genai
import time

# --- 1. SETUP KUNCI ---
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': pesan, 'parse_mode': 'Markdown'}
    requests.post(url, json=payload)

def ambil_harga_bitcoin():
    # KITA PAKAI COINGECKO (Lebih stabil untuk bot)
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return data['bitcoin']['usd']
    except Exception:
        # Cadangan jika CoinGecko sibuk, kita coba Binance lagi
        url_cadangan = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url_cadangan, timeout=10)
        data = response.json()
        return float(data['price'])

def analisis_ai(harga):
    prompt = f"""
    Kamu adalah trader profesional. Harga BTC sekarang ${harga}.
    Berikan komentar pasar 1 kalimat pendek yang berwibawa tentang level harga ini.
    Akhiri dengan emoji yang cocok.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "Pasar sedang volatile. Tetap waspada! ⚠️"

def main():
    try:
        # 1. Ambil Harga
        harga = ambil_harga_bitcoin()
        
        # 2. Analisis
        komentar = analisis_ai(harga)
        
        # 3. Kirim Laporan
        pesan = f"💎 **BITCOIN UPDATE**\nPrice: `${harga:,.2f}`\n\n💬 {komentar}"
        kirim_telegram(pesan)
        print("Sukses kirim laporan!")
        
    except Exception as e:
        print(f"Error: {e}")
        kirim_telegram(f"⚠️ Gagal ambil data: {e}")

if __name__ == "__main__":
    main()
