import streamlit as st
import requests

# Konfigurasi Halaman
st.set_page_config(
    page_title="Asisten Akademik Profesional - Hermes AI", 
    page_icon="🎓", 
    layout="centered"
)

# Sidebar untuk Informasi dan Kontrol Tambahan
with st.sidebar:
    st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=80)
    st.subheader("Tentang Aplikasi")
    st.write("Platform asisten akademik berbasis AI untuk membantu analisis studi, strategi kelulusan, dan konsultasi kurikulum.")
    st.markdown("---")
    
    # Tombol untuk mereset percakapan
    if st.button("🔄 Mulai Sesi Baru (Clear Chat)", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": "Kamu adalah asisten akademik perguruan tinggi yang profesional, ramah, dan solutif."},
            {"role": "assistant", "content": "Halo! Sesi baru telah dimulai. Ada hal akademik yang ingin kita diskusikan hari ini?"}
        ]
        st.rerun()

    st.markdown("### 💡 Tips Konsultasi")
    st.caption("- Tanyakan strategi perencanaan SKS.")
    st.caption("- Diskusikan estimasi kelulusan.")
    st.caption("- Konsultasikan topik tugas akhir.")

# Header Utama
st.title("🎓 Portal Konsultasi Akademik AI")
st.markdown("Silakan ajukan pertanyaan atau diskusikan permasalahan studimu dengan asisten pintar.")

# Ambil API Key secara aman
try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    API_KEY = ""

# Inisialisasi riwayat chat dengan System Prompt profesional
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Kamu adalah asisten akademik perguruan tinggi yang profesional, ramah, dan solutif."},
        {"role": "assistant", "content": "Halo! Saya asisten akademikmu yang ditenagai oleh model Hermes. Ada yang ingin didiskusikan tentang studimu?"}
    ]

# Tampilkan riwayat percakapan (kecuali system prompt agar tidak tampil di UI)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input Chat Pengguna
if prompt := st.chat_input("Tulis pertanyaan akademikmu di sini..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Proses respons dari AI
    with st.chat_message("assistant"):
        with st.spinner("AI sedang menganalisis..."):
            if not API_KEY:
                respon_ai = "⚠️ **Perhatian:** `OPENROUTER_API_KEY` belum terdeteksi di Streamlit Secrets."
            else:
                try:
                    headers = {
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://streamlit.io",
                        "X-Title": "Portal Akademik AI"
                    }
                    
                    payload = {
                        "model": "openrouter/free", 
                        "messages": st.session_state.messages
                    }
                    
                    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=30)
                    res_data = response.json()
                    
                    if "choices" in res_data and len(res_data["choices"]) > 0:
                        respon_ai = res_data["choices"][0]["message"]["content"]
                    else:
                        respon_ai = "Maaf, server AI sedang sibuk. Silakan coba beberapa saat lagi."
                        
                except Exception as e:
                    respon_ai = f"Terjadi kesalahan koneksi: {e}"
            
            st.markdown(respon_ai)
            
    st.session_state.messages.append({"role": "assistant", "content": respon_ai})
