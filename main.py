import google.generativeai as genai
import os
import requests

# --- SETUP ---
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

genai.configure(api_key=GEMINI_API_KEY)

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': pesan}
    requests.post(url, json=payload)

def cek_daftar_model():
    try:
        # Kita tanya ke Google: "Sebutkan model yang saya boleh pakai!"
        daftar_model = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Kita bersihkan namanya (hapus 'models/') biar rapi
                nama_bersih = m.name.replace('models/', '')
                daftar_model.append(nama_bersih)
        
        if not daftar_model:
            return "❌ GAWAT: Google bilang tidak ada model yang tersedia untuk API Key ini. Coba bikin Key baru di Google AI Studio."
            
        return "✅ MODEL YANG TERSEDIA:\n- " + "\n- ".join(daftar_model)

    except Exception as e:
        return f"⚠️ ERROR SAAT CEK MODEL:\n{e}"

if __name__ == "__main__":
    laporan = cek_daftar_model()
    kirim_telegram(laporan)
