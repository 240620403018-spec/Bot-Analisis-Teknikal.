import requests
import os

# --- AMBIL KUNCI ---
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']

print(f"➡️ Sedang mencoba kirim pesan ke ID: {CHAT_ID}")

def kirim_test():
    # Kita tes kirim pesan sederhana tanpa AI dulu
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    pesan = "🔔 TES KONEKSI: Halo bos! Jika pesan ini masuk, berarti setingan aman."
    
    payload = {
        'chat_id': CHAT_ID,
        'text': pesan
    }
    
    # Kirim Request
    response = requests.post(url, json=payload)
    
    # Cek Jawaban Telegram (Jujur-jujuran)
    print(f"➡️ Kode Status: {response.status_code}")
    print(f"➡️ Jawaban Telegram: {response.text}")
    
    if response.status_code == 200:
        print("✅ SUKSES! Pesan terkirim.")
    else:
        # Jika gagal, kita paksa Error agar GitHub jadi MERAH
        print("❌ GAGAL! Periksa 'Jawaban Telegram' di atas untuk tahu sebabnya.")
        raise Exception("Gagal mengirim pesan ke Telegram")

if __name__ == "__main__":
    kirim_test()
    
