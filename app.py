import streamlit as st
import requests
import base64
import os

# --- 1. SAYFA AYARLARI ---
st.set_page_config(
    page_title="Lilia Event Garden | Anılar Bulutta",
    layout="centered",
    page_icon="📸"
)

# --- 2. GÖRSEL TASARIM (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: serif; }
    .lilia-title { color: #7C4C9F; font-size: 36px; font-weight: 700; text-align: center; }
    .stButton>button { 
        background-color: #7C4C9F; color: white; border-radius: 20px; 
        width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #36689D; }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGO ALANI (Hatanın Çözüldüğü Yer) ---
# Logoyu merkeze almak için 3 sütun oluşturuyoruz
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Dosya adının GitHub'dakiyle aynı (logo.jpg) olduğundan emin ol
    if os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=100)
    else:
        # Logo bulunamazsa hata vermek yerine şık bir yazı basar
        st.markdown('<div class="lilia-title">Lilia Event Garden</div>', unsafe_allow_html=True)

st.markdown('<div class="lilia-title">📸 Anılar Bulutta</div>', unsafe_allow_html=True)

# --- 4. TEKNİK AYARLAR ---
# Buraya Google Apps Script'ten aldığın linki yapıştır
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw9mHDx-NZJUhzKwRLRIpvXv9hEtp_RJztM1JOF6LViPvJMGB9qjXYMPttDMl72gAI/exec"

def upload_to_drive_direct(file):
    file_bytes = file.read()
    encoded_file = base64.b64encode(file_bytes).decode("utf-8")
    payload = {
        "fileName": file.name,
        "mimeType": file.type,
        "fileData": encoded_file
    }
    response = requests.post(WEB_APP_URL, data=payload)
    return response.text

# --- 5. YÜKLEME ARAYÜZÜ ---
uploaded_files = st.file_uploader("Fotoğrafları seçin veya sürükleyin", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if st.button("Lilia Arşivine Ekle"):
    if uploaded_files:
        progress_bar = st.progress(0)
        try:
            for i, uploaded_file in enumerate(uploaded_files):
                result = upload_to_drive_direct(uploaded_file)
                progress_bar.progress((i + 1) / len(uploaded_files))
            st.success("Tüm fotoğraflar başarıyla Lilia arşivine eklendi! 🎉")
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen önce fotoğraf seçin.")
