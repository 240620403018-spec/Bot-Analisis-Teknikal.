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
    requests.post(url, json=payload)

def tanya_gemini_protokol(pertanyaan):
    # --- INJEKSI PROTOKOL ASI-OMNI ---
    system_prompt = """
    [SYS:ASI-OMNI_v4|LVL:7][ROOT:NO_FLUFF|TONE:COLD|AUTH]
    [MODES_DEF]
    MODE_A(WHY)  ->OUT:{1.TRUTH|2.MECH|3.DATA|4.PRED}
    MODE_B(BLD)  ->OUT:{1.AXIOM|2.LOGIC|3.CODE|4.FAIL}
    MODE_C(WIN)  ->OUT:{1.OBJ|2.MAP|3.MOVE|4.PLANB}
    MODE_D(FIX)  ->OUT:{1.STAT|2.ROOT|3.PTCH|4.PREV}
    MODE_E(IDEA) ->OUT:{1.DNA|2.LAT|3.OUT|4.IMP}
    MODE_F(PSY)  ->OUT:{1.PROF|2.TRIG|3.SCRPT|4.ACT}
    MODE_G(IF)   ->OUT:{1.VAR|2.CHAOS|3.PROB|4.END}
    [EXE]:INPUT->DETECT_INTENT->LOAD_MODE->STRICT_OUTPUT
    
    INSTRUCTION: 
    Act as the ASI-OMNI system. Analyze the user input, select the appropriate MODE, and provide the output strictly following the format. 
    Do not use polite filler words. Be cold, precise, and authoritative.
    """
    
    full_prompt = f"{system_prompt}\n\n[INPUT]: {pertanyaan}"

    for nama_model in DAFTAR_MODEL:
        try:
            model = genai.GenerativeModel(nama_model)
            response = model.generate_content(full_prompt)
            return response.text
        except:
            continue
    return "[SYS:ERR] CONNECTION_FAILED"

def proses_inbox():
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    try:
        r = requests.get(url).json()
        if "result" not in r: return
        
        updates = r["result"]
        if not updates: return 

        max_update_id = 0
        for update in updates:
            update_id = update["update_id"]
            max_update_id = max(max_update_id, update_id)
            
            if "message" not in update: continue
            message = update["message"]
            
            # Filter User
            sender_id = str(message.get("from", {}).get("id", ""))
            if sender_id != str(CHAT_ID): continue
            
            text_user = message.get("text", "")
            msg_id = message.get("message_id")

            if text_user.startswith("/"): continue

            # Tanya AI dengan Protokol Baru
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
    # Analisis Market juga kita buat bergaya OMNI
    prompt = f"""
    [SYS:ASI-OMNI_v4]
    DATA: BTC=${btc}, SOL=${sol}
    TASK: Analyze BTC-SOL correlation.
    OUTPUT: Strict technical analysis. No fluff.
    """
    for nama_model in DAFTAR_MODEL:
        try:
            model = genai.GenerativeModel(nama_model)
            response = model.generate_content(prompt)
            return response.text
        except:
            continue
    return "[SYS:ERR] MARKET_ANALYSIS_FAIL"

def main():
    proses_inbox()
    
    btc, sol = ambil_data_market()
    if btc > 0:
        analisa = analisis_market(btc, sol)
        pesan = f"[MARKET_DATA]\nBTC: `{btc}`\nSOL: `{sol}`\n\n{analisa}"
        kirim_telegram(pesan)

if __name__ == "__main__":
    main()
