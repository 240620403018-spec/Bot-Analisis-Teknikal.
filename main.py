import requests
import os
import google.generativeai as genai

# --- 1. MENGAMBIL KUNCI RAHASIA ---
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

# --- 2. SETUP OTAK GEMINI ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Target Aset (Bitcoin)
SYMBOL = "BTCUSDT"
URL_BINANCE = f"https://api.binance.com/api/v3/ticker/price?symbol={SYMBOL}"

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': pesan, 'parse_mode': 'Markdown'} 
    requests.post(url, json=payload)

def tanya_gemini_teknikal(harga):
    """
    Prompt ini dirancang untuk memaksa AI berpikir teknis.
    """
    prompt = f"""
    Anda adalah Senior Technical Analyst (Chartered Market Technician).
    Harga Bitcoin (BTC) saat ini berada di level: ${harga}.
    
    Tugas Anda:
    1. Analisis posisi harga ini terhadap level psikologis terdekat (misal: angka bulat seperti 90k, 95k, 100k).
    2. Berikan asumsi singkat tentang struktur pasar (Bullish/Bearish) berdasarkan harga tersebut.
    3. Gunakan istilah teknikal yang valid (contoh: Support, Resistance, Rejection, Breakout, Consolidation).
    4. JANGAN berikan saran keuangan, tapi berikan 'Bias Pasar'.
    
    Format Output (Singkat & Padat):
    📊 **STATUS TEKNIKAL**
    • Zona Harga: [Isi analisis]
    • Key Level: [Sebutkan angka terdekat]
    • Bias: [BULLISH / BEARISH / NEUTRAL]
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gagal melakukan analisis teknikal: {e}"

def cek_pasar():
    try:
        # Ambil Data
        response = requests.get(URL_BINANCE)
        data = response.json()
        harga = float(data['price'])
        
        # Analisis AI
        analisis = tanya_gemini_teknikal(harga)
        
        # Kirim Laporan
        pesan = f"🚨 **BTC/USDT UPDATE**\nPrice: `${harga:,.2f}`\n\n{analisis}"
        kirim_telegram(pesan)
        print("Analisis teknikal terkirim.")
        
    except Exception as e:
        print(f"System Error: {e}")

if __name__ == "__main__":
    cek_pasar()
  
