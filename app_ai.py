import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Konfigurasi Halaman Web
st.set_page_config(page_title="Prediksi Kelulusan AI", page_icon="🎓", layout="wide")

# --- KODE CSS KUSTOM UNTUK MEMPERCANTIK TAMPILAN ---
st.markdown("""
    <style>
    /* Mengatur latar belakang utama */
    .stApp {
        background-color: #f8f9fa;
    }
    /* Mempercantik kotak hasil prediksi */
    .card-sukses {
        padding: 20px;
        border-radius: 10px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
    }
    .card-gagal {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Header Utama Aplikasi
st.title("🎓 Dashboard Prediksi Kelulusan Siswa Berbasis AI")
st.markdown("Aplikasi cerdas untuk menganalisis peluang kelulusan berdasarkan kebiasaan harian siswa menggunakan **Deep Learning**.")
st.markdown("---")

# 1. MEMUAT MODEL AI DARI FILE TERSIMPAN
@st.cache_resource
def muat_otak_ai():
    return load_model("model_kelulusan.h5")

with st.spinner("🔄 Menghubungkan ke sistem otak AI..."):
    model = muat_otak_ai()

# 2. Panel Kontrol Sidebar yang Rapi
st.sidebar.markdown("## 🎛️ Panel Input Siswa")
st.sidebar.markdown("Sesuaikan parameter harian di bawah ini:")

jam_belajar = st.sidebar.slider("📚 Jumlah Jam Belajar (per hari):", 0.0, 10.0, 4.0, 0.1)
jam_tidur = st.sidebar.slider("💤 Jumlah Jam Tidur (per hari):", 0.0, 10.0, 6.0, 0.1)

st.sidebar.markdown("---")
tombol_prediksi = st.sidebar.button("🚀 Analisis Sekarang", type="primary", use_container_width=True)

# 3. Layout Utama (Dibagi menjadi 2 Kolom Seimbang)
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("📊 Panduan & Informasi Parameter")
    st.info("""
    **Cara Menggunakan Aplikasi:**
    1. Geser pengatur di panel sebelah kiri untuk menentukan **Jam Belajar** dan **Jam Tidur** siswa.
    2. Klik tombol **'Analisis Sekarang'** untuk melihat hasil keputusan AI.
    
    *Model ini dilatih menggunakan pola kebiasaan belajar dan istirahat untuk memprediksi tingkat keberhasilan.*
    """)
    
    # Menampilkan ringkasan input pengguna
    st.markdown("### 📝 Parameter Terpilih:")
    st.write(f"- **Jam Belajar:** {jam_belajar} Jam/hari")
    st.write(f"- **Jam Tidur:** {jam_tidur} Jam/hari")

with col2:
    st.subheader("🎯 Hasil Analisis & Keputusan AI")
    
    if tombol_prediksi:
        # Menyiapkan data masukan
        data_baru = np.array([[jam_belajar, jam_tidur]], dtype=float)
        
        # Proses prediksi
        prediksi_probabilitas = model.predict(data_baru, verbose=0)
        peluang_persen = prediksi_probabilitas[0][0] * 100
        
        # Menampilkan metrik keyakinan yang elegan
        st.metric(label="📈 Tingkat Keyakinan (Peluang Lulus)", value=f"{peluang_persen:.2f}%")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Keputusan Akhir dengan Kotak Kustom
        if peluang_persen > 50:
            st.markdown('<div class="card-sukses">🎉 KEPUTUSAN AKHIR: LULUS!<br><span style="font-size:14px; font-weight:normal;">Siswa memiliki pola belajar yang sangat ideal!</span></div>', unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown('<div class="card-gagal">❌ KEPUTUSAN AKHIR: GAGAL!<br><span style="font-size:14px; font-weight:normal;">Siswa disarankan untuk menambah durasi jam belajar.</span></div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Belum ada analisis yang dijalankan. Silakan klik tombol **'Analisis Sekarang'** di panel kiri.")