import streamlit as st
import requests
import base64

# Sayfa Ayarları
st.set_page_config(page_title="Lilia - Anılar Bulutta", layout="centered", page_icon="📸")

st.markdown("""
<div style='text-align: center;'>
    <h1>📸 Anılar Bulutta</h1>
    <p>Lilia Organizasyon etkinliklerinden en güzel kareleri bizimle paylaşın!</p>
</div>
""", unsafe_allow_html=True)

# 1. Adımda kopyaladığın o uzun linki buradaki tırnakların içine yapıştır:
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw9mHDx-NZJUhzKwRLRIpvXv9hEtp_RJztM1JOF6LViPvJMGB9qjXYMPttDMl72gAI/exec"

def upload_to_drive_direct(file):
    file_bytes = file.read()
    encoded_file = base64.b64encode(file_bytes).decode("utf-8")
    
    payload = {
        "fileName": file.name,
        "mimeType": file.type,
        "fileData": encoded_file
    }
    
    # Doğrudan senin Drive arka kapına gönderiyoruz
    response = requests.post(WEB_APP_URL, data=payload)
    return response.text

# Dosya Yükleme Arayüzü
uploaded_files = st.file_uploader("Fotoğrafları seçmek için tıklayın veya buraya sürükleyin", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if st.button("Seçilen Fotoğrafları Yükle", type="primary"):
    if uploaded_files:
        with st.spinner('Fotoğraflar buluta aktarılıyor, lütfen bekleyin...'):
            try:
                for uploaded_file in uploaded_files:
                    result = upload_to_drive_direct(uploaded_file)
                    if "Hata" in result:
                        st.error(f"Dosya yüklenirken bir sorun oluştu: {result}")
                    
                st.success("Tüm fotoğraflar başarıyla Lilia arşivine eklendi! Teşekkür ederiz. 🎉")
            except Exception as e:
                st.error(f"Sistemsel bir hata oluştu: {e}")
    else:
        st.warning("Lütfen önce fotoğraf seçin.")