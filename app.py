import streamlit as st
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload
import io
import json

# Sayfa Ayarları (Vitrin tasarımı)
st.set_page_config(page_title="Lilia - Anılar Bulutta", layout="centered", page_icon="📸")

st.markdown("""
<div style='text-align: center;'>
    <h1>📸 Anılar Bulutta</h1>
    <p>Lilia Organizasyon etkinliklerinden en güzel kareleri bizimle paylaşın!</p>
</div>
""", unsafe_allow_html=True)

# Google Drive Bağlantısı (Arka planda çalışacak güvenlik kısmı)
@st.cache_resource
def get_drive_service():
    # Streamlit Secrets'dan anahtarı al
    secrets_dict = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(
        secrets_dict,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    return build('drive', 'v3', credentials=credentials)

# Yükleme Fonksiyonu
def upload_to_drive(file, folder_id):
    service = get_drive_service()
    file_metadata = {
        'name': file.name,
        'parents': [folder_id]
    }
    media = MediaIoBaseUpload(io.BytesIO(file.read()), mimetype=file.type)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

# --- ÖNEMLİ: Kendi Klasör ID'ni buraya yapıştır ---
FOLDER_ID = "1XDsbMMY_40xMOT-ujkXb4NOkLjjNXIVi"

# Dosya Yükleme Arayüzü
uploaded_files = st.file_uploader("Fotoğrafları seçmek için tıklayın veya buraya sürükleyin", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if st.button("Seçilen Fotoğrafları Yükle", type="primary"):
    if uploaded_files:
        with st.spinner('Fotoğraflar yükleniyor, lütfen bekleyin...'):
            try:
                for uploaded_file in uploaded_files:
                    upload_to_drive(uploaded_file, FOLDER_ID)
                st.success("Tüm fotoğraflar başarıyla Lilia arşivine eklendi! Teşekkür ederiz. 🎉")
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Lütfen önce fotoğraf seçin.")