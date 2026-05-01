import streamlit as st
import requests
import base64

# --- 1. SAYFA AYARLARI ---
st.set_page_config(
    page_title="Lilia Event Garden | Anılar Bulutta",
    layout="centered",
    page_icon="📸"
)

# --- 2. GÖRSEL TASARIM (CSS) ---
# Buton rengini belirgin şekilde açtık ve yazı rengini koyulaştırdık.
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
    }
    .stApp { 
        background-color: #FFFFFF; 
        color: #000000; 
        font-family: serif; 
    }
    .lilia-title { 
        color: #7D3C98; 
        font-size: 36px; 
        font-weight: 700; 
        text-align: center; 
        margin-bottom: 30px;
    }
    /* Buton Tasarımı: Çok açık lila arka plan, koyu mor yazı */
    .stButton>button { 
        background-color: #E8DAEF; /* Çok açık, ferah bir lila */
        color: #4A235A; /* Koyu mor yazı (okunabilirlik için) */
        border: 2px solid #7D3C98; 
        border-radius: 30px; 
        width: 100%; 
        padding: 15px;
        font-weight: bold;
        font-size: 20px;
        transition: 0.3s;
    }
    .stButton>button:hover { 
        background-color: #D2B4DE; /* Üzerine gelince biraz daha koyulaşır */
        color: #4A235A;
        border-color: #4A235A;
    }
    /* Dosya yükleme alanı */
    .stFileUploader {
        border: 2px dashed #D2B4DE;
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. BAŞLIK ---
st.markdown('<div class="lilia-title">📸 Anılar Bulutta</div>', unsafe_allow_html=True)

# --- 4. TEKNİK AYARLAR ---
# Google Apps Script URL'ni buraya yapıştırmayı unutma
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

# --- 5. ARAYÜZ ---
uploaded_files = st.file_uploader("Fotoğrafları seçin veya sürükleyin", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

st.write("") # Boşluk

if st.button("Fotoğrafları Arşive Gönder"):
    if uploaded_files:
        progress_bar = st.progress(0)
        try:
            for i, uploaded_file in enumerate(uploaded_files):
                result = upload_to_drive_direct(uploaded_file)
                progress_bar.progress((i + 1) / len(uploaded_files))
            st.success("Tüm fotoğraflar başarıyla arşive eklendi! 🎉")
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen önce fotoğraf seçin.")
