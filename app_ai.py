import streamlit as st
import requests

st.set_page_config(page_title="Asisten Akademik Hermes AI", page_icon="💬", layout="centered")

st.title("💬 Konsultasi Akademik dengan Hermes AI")
st.write("Tanyakan seputar strategi kelulusan, analisis IPK, atau tips perkuliahan langsung dengan AI.")

# Konfigurasi API (Kamu bisa memasukkan API Key dari penyedia seperti OpenRouter)
# Disarankan menggunakan st.secrets untuk keamanan kunci API di Streamlit Cloud
API_KEY = st.secrets.get("OPENROUTER_API_KEY", "MASUKKAN_API_KEY_KAMU_DI_SINI")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Saya asisten akademikmu yang ditenagai oleh model Hermes. Ada yang ingin didiskusikan tentang studimu?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ketik pertanyaan atau data akademikmu di sini..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Hermes AI sedang merespons..."):
            try:
                # Menggunakan endpoint API (Contoh via OpenRouter untuk Nous Hermes)
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "nousresearch/hermes-3-llama-3-8b", # Contoh model Hermes
                    "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                }
                
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=30)
                res_data = response.json()
                
                if "choices" in res_data:
                    respon_ai = res_data["choices"][0]["message"]["content"]
                else:
                    respon_ai = "Maaf, terjadi kendala saat menghubungi server AI. Pastikan API Key sudah terpasang dengan benar."
            except Exception as e:
                respon_ai = f"Terjadi kesalahan koneksi: {e}"
            
            st.markdown(respon_ai)
            
    st.session_state.messages.append({"role": "assistant", "content": respon_ai})
