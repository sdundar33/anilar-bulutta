import streamlit as st
import requests
import base64

# --- TASARIM VE SAYFA AYARLARI ---
st.set_page_config(
    page_title="Lilia Event Garden | Anılar Bulutta",
    layout="centered",
    page_icon="📸"
)

# Lilia Kurumsal Renkleri (Görselden Alındı)
LILIA_PURPLE = "#7C4C9F" # Logodaki mor
LILIA_BLUE = "#36689D"   # Kuşun kanatlarındaki mavi

# CSS ile Görsel Düzenleme
st.markdown(f"""
<style>
    .stApp {{
        background-color: #FFFFFF;
    }}
    .lilia-header {{
        color: {LILIA_PURPLE};
        font-family: 'serif';
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 0px;
    }}
    .lilia-subheader {{
        color: #333333;
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }}
    .stButton>button {{
        background-color: {LILIA_PURPLE};
        color: white;
        border-radius: 25px;
        width: 100%;
        height: 50px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background-color: {LILIA_BLUE};
        border-color: {LILIA_BLUE};
    }}
</style>
""", unsafe_allow_html=True)

# Üst Görsel (Lilia Logosu ve Kuş Figürü)
st.image("https://raw.githubusercontent.com/username/repo/main/image_0.png", use_column_width=True) # Buraya depondaki görselin ham linkini koyabilirsin

st.markdown('<p class="lilia-header">LILIA EVENT GARDEN</p>', unsafe_allow_html=True)
st.markdown('<p class="lilia-subheader">Anılar Bulutta: En güzel karelerinizi bizimle paylaşın.</p>', unsafe_allow_html=True)

# --- FONKSİYONEL KISIM (DEĞİŞTİRME) ---
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

# Yükleme Alanı
uploaded_files = st.file_uploader("", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if st.button("LİLİA ARŞİVİNE GÖNDER"):
    if uploaded_files:
        with st.spinner('Fotoğraflarınız yükleniyor...'):
            try:
                for uploaded_file in uploaded_files:
                    upload_to_drive_direct(uploaded_file)
                st.success("Tüm anılarınız başarıyla kaydedildi. Teşekkür ederiz! 🎉")
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen önce bir dosya seçin.")
