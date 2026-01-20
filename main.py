import requests
import os
import google.generativeai as genai

# --- 1. AMBIL KUNCI RAHASIA ---
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

# --- 2. SETUP OTAK GEMINI ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    # Kita pakai Markdown agar tulisan bisa tebal/miring
    payload = {'chat_id': CHAT_ID, 'text': pesan, 'parse_mode': 'Markdown'} 
    requests.post(url, json=payload)

def analisis_teknikal(harga):
    prompt = f"""
    Kamu adalah Senior Technical Analyst.
    Harga Bitcoin (BTC) saat ini: ${harga}.
    
    Berikan update pasar singkat (maksimal 50 kata) dengan gaya profesional:
    1. Tentukan Bias (Bullish/Bearish/Sideways).
    2. Sebutkan Key Level (Support/Resistance) terdekat.
    3. Rekomendasi singkat (Wait and See / Accumulate / Take Profit).
    
    Gunakan emoji yang relevan.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Maaf, AI sedang pusing: {e}"

def cek_pasar():
    try:
        # 1. Ambil Harga Real-time Binance
        r = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT")
        data = r.json()
        harga = float(data['price'])
        
        # 2. Minta Pendapat AI
        hasil_analisis = analisis_teknikal(harga)
        
        # 3. Kirim Laporan
        pesan_final = f"🚨 **BTC MARKET ALERT**\nPrice: `${harga:,.2f}`\n\n{hasil_analisis}"
        kirim_telegram(pesan_final)
        print("Laporan terkirim!")
        
    except Exception as e:
        print(f"Error: {e}")
        # Kirim notifikasi error ke HP jika ada masalah fatal
        kirim_telegram(f"⚠️ Bot Error: {e}")

if __name__ == "__main__":
    cek_pasar()
