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
    /* Uygulamanın en üstündeki boşluğu sıfırlıyoruz */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stApp { 
        background-color: #FFFFFF; 
        color: #000000; 
        font-family: serif; 
    }
    .lilia-title { 
        color: #7C4C9F; 
        font-size: 28px; 
        font-weight: 700; 
        text-align: center; 
        margin-top: 5px;
    }
    .stButton>button { 
        background-color: #9B59B6; 
        color: white; 
        border-radius: 25px; 
        border: none;
        width: 100%; 
        padding: 12px;
        font-weight: bold;
        transition: 0.4s;
    }
    .stButton>button:hover { 
        background-color: #AF7AC5; 
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGO ALANI (Yukarı Taşınmış ve Küçültülmüş) ---
# Logoyu tam merkeze ve en yukarıya alıyoruz
col1, col2, col3 = st.columns([2, 1, 2]) # Orta sütunu daha daralttık ki 80px tam ortalansın

with col2:
    if os.path.exists("logo.jpg"):
        # Boyutu 80'e çektik
        st.image("logo.jpg", width=80)
    else:
        st.markdown('<h4 style="text-align: center; color: #7C4C9F;">Lilia</h4>', unsafe_allow_html=True)

st.markdown('<div class="lilia-title">📸 Anılar Bulutta</div>', unsafe_allow_html=True)

# --- 4. TEKNİK AYARLAR ---
# Buraya Google Apps Script'ten aldığın linki tekrar yapıştırmayı unutma
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
