import streamlit as st
import requests

# Konfigurasi Halaman
st.set_page_config(
    page_title="Portal Konsultasi ASISTEN AKADEMIK", 
    page_icon="🎓", 
    layout="centered"
)

# Custom CSS untuk Estetika Akademik Profesional (Warm Ivory & Deep Navy)
st.markdown("""
    <style>
    /* Latar belakang utama: Warna gading/ivory hangat ala perpustakaan akademik */
    .stApp {
        background-color: #f7f5f0;
        color: #2c3e50;
    }
    
    /* Warna teks umum agar kontras dan tajam */
    .stApp p, .stApp span, .stApp label, .stMarkdown {
        color: #2c3e50 !important;
    }

    /* Styling Sidebar: Biru navy gelap berwibawa khas institusi */
    [data-testid="stSidebar"] {
        background-color: #1b263b;
        border-right: 1px solid #d1d5db;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] div {
        color: #e0e1dd !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #415a77;
    }

    /* Kotak Input Chat */
    .stChatInputContainer input {
        background-color: #ffffff !important;
        color: #1b263b !important;
        border-radius: 10px !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    /* Tombol Kustom ala Buku/Jurnal */
    .stButton button {
        border-radius: 6px;
        font-weight: 500;
        background-color: #415a77;
        color: #ffffff;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #778da9;
        color: #ffffff;
    }

    /* Judul Utama dengan sentuhan klasik */
    h1, h2, h3 {
        color: #1b263b !important;
        font-family: 'Georgia', serif;
        font-weight: 700;
        letter-spacing: -0.3px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar untuk Informasi dan Kontrol
with st.sidebar:
    st.image("https://img.icons8.com/color/96/books.png", width=70)
    st.subheader("Navigasi Sesi")
    st.write("Gunakan layanan konsultasi ini untuk membantumu merencanakan studi dengan lebih terarah.")
    st.markdown("---")
    
    # Tombol Reset Chat
    if st.button("🔄 Mulai Percakapan Baru", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": "Kamu adalah asisten akademik perguruan tinggi yang profesional, ramah, dan solutif."},
            {"role": "assistant", "content": "Halo! Sesi baru telah dimulai. Ada hal akademik yang ingin kita diskusikan hari ini?"}
        ]
        st.rerun()

    st.markdown("### 📌 Panduan Singkat")
    st.caption("1. Ketik pertanyaan seputar SKS/IPK.")
    st.caption("2. Minta tips strategi kelulusan.")
    st.caption("3. Konsultasikan draf tugas akhir.")

# Header Utama Aplikasi
st.title("🎓 ASISTEN AKADEMIK")
st.markdown("Platform konsultasi terpadu untuk mendukung perencanaan dan pencapaian studimu.")
st.markdown("---")

# Ambil API Key secara aman dari Streamlit Secrets
try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    API_KEY = ""

# Inisialisasi riwayat chat dengan System Prompt profesional di belakang layar
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Kamu adalah asisten akademik perguruan tinggi yang profesional, ramah, dan solutif."},
        {"role": "assistant", "content": "Halo! Saya Asisten Akademikmu. Ada yang ingin didiskusikan tentang studimu?"}
    ]

# Tampilkan riwayat percakapan (menyembunyikan system prompt dari UI)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input Chat Pengguna
if prompt := st.chat_input("Tulis pertanyaan atau analisis akademikmu di sini..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Proses respons dari server
    with st.chat_message("assistant"):
        with st.spinner("Sedang memproses analisis..."):
            if not API_KEY:
                respon_ai = "⚠️ **Perhatian:** `OPENROUTER_API_KEY` belum terdeteksi di Streamlit Secrets."
            else:
                try:
                    headers = {
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://streamlit.io",
                        "X-Title": "Portal Akademik"
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
                        respon_ai = "Maaf, sistem sedang sibuk. Silakan coba beberapa saat lagi."
                        
                except Exception as e:
                    respon_ai = f"Terjadi kesalahan koneksi: {e}"
            
            st.markdown(respon_ai)
            
    st.session_state.messages.append({"role": "assistant", "content": respon_ai})
