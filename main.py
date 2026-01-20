import requests
import os
import google.generativeai as genai
import time

# --- SETUP ---
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

genai.configure(api_key=GEMINI_API_KEY)

DAFTAR_MODEL = [
    'gemini-2.0-flash-lite-preview-02-05',
    'gemini-flash-latest',
    'gemini-2.0-flash-exp',
    'gemini-1.5-flash'
]

def kirim_telegram(pesan, reply_to_id=None):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': pesan, 'parse_mode': 'Markdown'}
    if reply_to_id: payload['reply_to_message_id'] = reply_to_id
    try:
        requests.post(url, json=payload)
    except:
        pass

def tanya_gemini(text_input):
    prompt = f"[SYS:ASI-OMNI][MODE:CHAT]\nUSER: {text_input}\nOUT: INDONESIAN, COLD, SHORT."
    for nama_model in DAFTAR_MODEL:
        try:
            model = genai.GenerativeModel(nama_model)
            response = model.generate_content(prompt)
            return response.text
        except:
            continue
    return "⚠️ AI Error."

def proses_inbox():
    # 1. Ambil Update
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    try:
        resp = requests.get(url).json()
    except:
        return # Gagal koneksi, berhenti dulu

    if "result" not in resp: return
    updates = resp["result"]
    if not updates: return 

    max_id = 0
    
    # 2. Loop Pesan
    for update in updates:
        update_id = update["update_id"]
        max_id = max(max_id, update_id)
        
        if "message" not in update: continue
        msg = update["message"]
        
        # Cek Pengirim
        sender = str(msg.get("from", {}).get("id", ""))
        if sender != str(CHAT_ID): continue
        
        text = msg.get("text", "")
        msg_id = msg.get("message_id")
        
        if not text.startswith("/"):
            # Jawab Chat
            jawaban = tanya_gemini(text)
            kirim_telegram(jawaban, reply_to_id=msg_id)

    # 3. Hapus Pesan Lama (Mark as Read)
    # BAGIAN INI YANG TADI ERROR, SUDAH SAYA PERBAIKI POSISINYA
    if max_id > 0:
        requests.get(url, params={'offset': max_id + 1})

def cek_market_sniper():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,solana&vs_currencies=usd"
        data = requests.get(url, timeout=10).json()
        btc = data['bitcoin']['usd']
        sol = data['solana']['usd']
        
        prompt = f"""
        [SYS:ASI-OMNI][MODE:SNIPER]
        DATA: BTC=${btc}, SOL=${sol}
        OUTPUT:
        [MODE_C: STRATEGY]
        [PLAN_BTC] Action/Entry/Target/Cut
        [PLAN_SOL] Action/Entry/Target/Cut
        [EXECUTION] Saran Final (Indo)
        """
        analisa = tanya_gemini(prompt)
        kirim_telegram(f"💀 **SNIPER SIGNAL**\n{analisa}")
    except:
        pass

def main():
    proses_inbox()
    cek_market_sniper()

if __name__ == "__main__":
    main()
    except Exception as e:
        print(f"Inbox Error: {e}")

def main():
    # 1. Cek Pesan
    proses_inbox()
    
    # 2. Cek Market
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,solana&vs_currencies=usd"
        data = requests.get(url, timeout=10).json()
        btc = data['bitcoin']['usd']
        sol = data['solana']['usd']
        
        # --- ANALISIS SNIPER ---
        prompt_analisis = f"""
        [SYS:ASI-OMNI_v4][MODE:SNIPER]
        DATA: BTC=${btc}, SOL=${sol}
        OUTPUT:
        [MODE_C: STRATEGY]
        [PLAN_BTC] Action/Entry/Target/Cut
        [PLAN_SOL] Action/Entry/Target/Cut
        [EXECUTION] Saran Final (Bahasa Indonesia)
        """
        
        analisa = tanya_gemini(prompt_analisis)
        kirim_telegram(f"💀 **SNIPER SIGNAL**\n{analisa}")
        
    except:
        print("Gagal ambil data market")

if __name__ == "__main__":
    main()
        if max_update_id > 0:
            requests.get(url, params={'offset': max_update_id + 1})
            
    except Exception as e:
        print(f"Error inbox: {e}")

def ambil_data_market():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,solana&vs_currencies=usd"
        r = requests.get(url, timeout=10)
        data = r.json()
        return data['bitcoin']['usd'], data['solana']['usd']
    except:
        return 0, 0

def analisis_sinyal_sniper(btc, sol):
    prompt = f"""
    [SYS:ASI-OMNI_v4|LVL:7][ROOT:TRADING_CORE]
    
    LIVE DATA:
    - BTC: ${btc}
    - SOL: ${sol}
    
    MISSION:
    Generate precision TRADING PLAN based on current price structure.
    
    OUTPUT FORMAT (STRICT INDONESIAN | MONOSPACE BLOCKS):
    
    [MODE_C: STRATEGY]
    [MARKET_SENTIMENT]: (BULLISH / BEARISH / NEUTRAL)
    [CORRELATION]: (Explain BTC influence on SOL briefly)
        if max_update_id > 0:
            requests.get(url, params={'offset': max_update_id + 1})
            
    except Exception as e:
        print(f"Error inbox: {e}")

def ambil_data_market():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,solana&vs_currencies=usd"
        r = requests.get(url, timeout=10)
        data = r.json()
        return data['bitcoin']['usd'], data['solana']['usd']
    except:
        return 0, 0

def analisis_sinyal_sniper(btc, sol):
    # --- PROTOKOL SINYAL TRADING (SNIPER MODE) ---
    prompt = f"""
    [SYS:ASI-OMNI_v4|LVL:7][ROOT:TRADING_CORE]
    
    LIVE DATA:
    - BTC: ${btc}
    - SOL: ${sol}
    
    MISSION:
    Generate precision TRADING PLAN based on current price structure.
    
    OUTPUT FORMAT (STRICT INDONESIAN | MONOSPACE BLOCKS):
    
    [MODE_C: STRATEGY]
    [MARKET_SENTIMENT]: (BULLISH / BEARISH / NEUTRAL)
    [CORRELATION]: (Explain BTC influence on SOL briefly)
    
    [PLAN_BTC] ($ {btc})
    > ACTION : (LONG / SHORT / WAIT)
    > ENTRY  : (Best price to enter)
    > TARGET : (Take Profit Level)
    > CUT    : (Stop Loss Level)
    
    [PLAN_SOL] ($ {sol})
    > ACTION : (LONG / SHORT / WAIT)
    > ENTRY  : (Best price to enter)
    > TARGET : (Take Profit Level)
    > CUT    : (Stop Loss Level)
    
    [EXECUTION]: (Final direct command)
    """
    
    for nama_model in DAFTAR_MODEL:
        try:
            model = genai.GenerativeModel(nama_model)
            response = model.generate_content(prompt)
            return response.text
        except:
            continue
    return "[SYS:ERR] SIGNAL_GENERATION_FAILED"

def main():
    # 1. Jawab Chat Dulu
    proses_inbox()
    
    # 2. Analisis Sinyal
    btc, sol = ambil_data_market()
    if btc > 0:
        analisa = analisis_sinyal_sniper(btc, sol)
        # Header simple saja, biarkan isinya yang bicara
        pesan = f"💀 **ASI-OMNI LIVE SIGNAL**\n\n{analisa}"
        kirim_telegram(pesan)

if __name__ == "__main__":
    main()
            sender_id = str(message.get("from", {}).get("id", ""))
            if sender_id != str(CHAT_ID): continue
            
            text_user = message.get("text", "")
            msg_id = message.get("message_id")

            if text_user.startswith("/"): continue

            # Tanya AI
            jawaban = tanya_gemini_protokol(text_user)
            kirim_telegram(f"{jawaban}", reply_to_id=msg_id)

        # Mark as read
        if max_update_id > 0:
            requests.get(url, params={'offset': max_update_id + 1})
            
    except Exception as e:
        print(f"Error inbox: {e}")

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
    [SYS:ASI-OMNI_v4]
    DATA: BTC=${btc}, SOL=${sol}
    TASK: Analisis korelasi BTC-SOL.
    OUTPUT: Analisis teknikal ketat dalam BAHASA INDONESIA. Tanpa basa-basi.
    """
    for nama_model in DAFTAR_MODEL:
        try:
            model = genai.GenerativeModel(nama_model)
            response = model.generate_content(prompt)
            return response.text
        except:
            continue
    return "[SYS:ERR] ANALISIS_GAGAL"

def main():
    proses_inbox()
    
    btc, sol = ambil_data_market()
    if btc > 0:
        analisa = analisis_market(btc, sol)
        pesan = f"[MARKET_DATA]\nBTC: `{btc}`\nSOL: `{sol}`\n\n{analisa}"
        kirim_telegram(pesan)

if __name__ == "__main__":
    main()
