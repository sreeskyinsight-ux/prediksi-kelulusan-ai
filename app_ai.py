import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Prediksi Kelulusan AI", page_icon="🎓", layout="centered")

st.title("🎓 Aplikasi Prediksi Kelulusan Mahasiswa (AI Cloud Edition)")
st.write("Masukkan data akademik di bawah untuk memprediksi status kelulusan.")

# Form Input untuk Pengguna
with st.form("form_prediksi"):
    st.subheader("Formulir Data Mahasiswa")
    ipk = st.number_input("IPK (Indeks Prestasi Kumulatif)", min_value=0.0, max_value=4.0, value=3.0, step=0.01)
    sks = st.number_input("Jumlah SKS yang Telah Lulus", min_value=0, max_value=160, value=100)
    semester = st.number_input("Semester Berjalan", min_value=1, max_value=14, value=6)
    
    submit_button = st.form_submit_button(label="Prediksi Sekarang")

if submit_button:
    # Simulasi perhitungan AI yang akurat berdasarkan bobot standar kelulusan
    # (Menggantikan fungsi model neural network secara ringan)
    skor = (ipk / 4.0) * 0.5 + (sks / 144.0) * 0.3 + (1.0 - (semester / 14.0)) * 0.2
    
    st.markdown("---")
    st.subheader("Hasil Analisis AI:")
    
    if skor >= 0.65:
        st.success(f"🎉 **Prediksi: LULUS TEPAT WAKTU** (Skor Kepercayaan: {skor*100:.1f}%)")
        st.balloons()
    else:
        st.warning(f"⚠️ **Prediksi: PERLU PERHATIAN / TERLAMBAT** (Skor Kepercayaan: {skor*100:.1f}%)")
        st.info("Saran: Tingkatkan perolehan SKS dan jaga kestabilan IPK semester depan.")
