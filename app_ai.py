import streamlit as st
import requests

st.set_page_config(page_title="Asisten Akademik Hermes AI", page_icon="💬", layout="centered")

st.title("💬 Konsultasi Akademik dengan Hermes AI")
st.write("Tanyakan seputar strategi kelulusan, analisis IPK, atau tips perkuliahan langsung dengan AI.")

# Mengambil API Key dari Streamlit Secrets secara aman
try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    API_KEY = ""

# Inisialisasi riwayat chat di sesi Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Saya asisten akademikmu yang ditenagai oleh model AI. Ada yang ingin didiskusikan tentang studimu?"}
    ]

# Tampilkan riwayat percakapan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kotak input chat
if prompt := st.chat_input("Ketik pertanyaan atau data akademikmu di sini..."):
    # Simpan dan tampilkan pesan pengguna
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Proses respons dari AI
    with st.chat_message("assistant"):
        with st.spinner("AI sedang merespons..."):
            if not API_KEY or API_KEY == "MASUKKAN_API_KEY_KAMU_DI_DISINI":
                respon_ai = "⚠️ **Perhatian:** `OPENROUTER_API_KEY` belum terdeteksi di Streamlit Secrets. Silakan masukkan kunci API kamu di menu Settings > Secrets pada dashboard Streamlit Cloud."
            else:
                try:
                    headers = {
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://streamlit.io", # Opsional untuk OpenRouter
                        "X-Title": "Asisten Akademik AI"         # Opsional untuk OpenRouter
                    }
                    
                    # Menggunakan router otomatis openrouter/free untuk menghindari error nama model
                    payload = {
                        "model": "openrouter/free", 
                        "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                    }
                    
                    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=30)
                    res_data = response.json()
                    
                    if "choices" in res_data and len(res_data["choices"]) > 0:
                        respon_ai = res_data["choices"][0]["message"]["content"]
                    elif "error" in res_data:
                        respon_ai = f"Gagal dari server AI: {res_data['error'].get('message', 'Terjadi kesalahan tidak dikenal.')}"
                    else:
                        respon_ai = f"Respon tidak valid dari server. Data: {res_data}"
                        
                except Exception as e:
                    respon_ai = f"Terjadi kesalahan koneksi: {e}"
            
            st.markdown(respon_ai)
            
    # Simpan riwayat respons asisten
    st.session_state.messages.append({"role": "assistant", "content": respon_ai})
