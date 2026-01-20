import requests
import os
import google.generativeai as genai
import time

# --- SETUP ---
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID'] # ID Anda (agar bot hanya nurut sama Anda)
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

genai.configure(api_key=GEMINI_API_KEY)

# DAFTAR MODEL (Agar tidak mogok)
DAFTAR_MODEL = [
    'gemini-2.0-flash-lite-preview-02-05',
    'gemini-flash-latest',
    'gemini-2.0-flash-exp',
    'gemini-1.5-flash'
]

def kirim_telegram(pesan, reply_to_id=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID, 
        'text': pesan, 
        'parse_mode': 'Markdown'
    }
    if reply_to_id:
        payload['reply_to_message_id'] = reply_to_id
        
    requests.post(url, json=payload)

def tanya_gemini(pertanyaan):
    prompt = f"""
    Kamu adalah Asisten Crypto Pribadi. Jawab pertanyaan user ini dengan ringkas, santai, dan cerdas.
    User bertanya: "{pertanyaan}"
    """
    for nama_model in DAFTAR_MODEL:
        try:
            model = genai.GenerativeModel(nama_model)
            response = model.generate_content(prompt)
            return response.text
        except:
            continue
    return "Maaf bos, otak saya lagi error koneksi."

def proses_inbox():
    # 1. Cek Pesan Masuk (Inbox)
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    try:
        r = requests.get(url).json()
        if "result" not in r: return
        
        updates = r["result"]
        if not updates: return # Gak ada pesan baru

        max_update_id = 0
        
        # 2. Baca satu per satu
        for update in updates:
            update_id = update["update_id"]
            max_update_id = max(max_update_id, update_id)
            
            if "message" not in update: continue
            message = update["message"]
            
            # Cek pengirim (Hanya balas pesan dari Anda, bukan orang asing)
            # Kita bandingkan dengan str(CHAT_ID)
            sender_id = str(message.get("from", {}).get("id", ""))
            
            if sender_id != str(CHAT_ID):
                continue # Abaikan pesan orang lain
            
            text_user = message.get("text", "")
            msg_id = message.get("message_id")

            # Jangan balas perintah /start
            if text_user.startswith("/"): continue

            # 3. Tanya Gemini
            print(f"📩 Ada pertanyaan: {text_user}")
            jawaban = tanya_gemini(text_user)
            
            # 4. Kirim Balasan
            kirim_telegram(f"🤖 **JAWABAN AI:**\n{jawaban}", reply_to_id=msg_id)

        # 5. HAPUS PESAN LAMA (Agar tidak dibalas ulang terus-menerus)
        # Kita panggil getUpdates lagi dengan offset baru untuk "Mark as Read"
        if max_update_id > 0:
            requests.get(url, params={'offset': max_update_id + 1})
            
    except Exception as e:
        print(f"Error baca inbox: {e}")

# --- FUNGSI MARKET SEBELUMNYA ---
def ambil_data_market():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,solana&vs_currencies=usd"
        r = requests.get(url, timeout=10)
        data = r.json()
        return data['bitcoin']['usd'], data['solana']['usd']
    except:
        return 0, 0

def analisis_market(btc, sol):
    prompt = f"""
    Analisa singkat market crypto (Bahasa Indo):
    BTC: ${btc:,.0f}, SOL: ${sol:,.0f}.
    Fokus ke korelasi BTC-SOL. Sinyal Bullish/Bearish?
    Buat dalam tabel Markdown.
    """
    for nama_model in DAFTAR_MODEL:
        try:
            model = genai.GenerativeModel(nama_model)
            response = model.generate_content(prompt)
            return response.text
        except:
            continue
    return "Gagal analisis."

def main():
    # TUGAS 1: Jawab pertanyaan user dulu (Prioritas)
    proses_inbox()
    
    # TUGAS 2: Lanjut kirim update market rutin
    btc, sol = ambil_data_market()
    if btc > 0:
        analisa = analisis_market(btc, sol)
        pesan = f"🔥 **MARKET UPDATE**\nBTC: `${btc}` | SOL: `${sol}`\n\n{analisa}"
        kirim_telegram(pesan)

if __name__ == "__main__":
    main()
