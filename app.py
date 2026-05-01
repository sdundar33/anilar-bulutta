import streamlit as st
import requests
import base64

# --- 1. SAYFA AYARLARI ---
st.set_page_config(
    page_title="Lilia Event Garden | Anılar Bulutta",
    layout="centered",
    page_icon="📸"
)

# --- 2. GÖRSEL TASARIM (KESİN ÇÖZÜM CSS) ---
st.markdown("""
<style>
    /* Sayfayı aşağı kaydırıyoruz */
    .block-container {
        padding-top: 6rem !important;
    }
    
    .stApp { 
        background-color: #FFFFFF !important; 
    }

    /* Başlık: Zarif Mor */
    .lilia-title { 
        color: #7D3C98 !important; 
        font-size: 34px !important; 
        font-weight: 700 !important; 
        text-align: center !important; 
        margin-bottom: 40px !important;
        font-family: serif !important;
    }

    /* DOSYA YÜKLEME ALANI (Siyahlığı Bitiren Kısım) */
    /* Dış çerçeve ve iç bölmeyi tek vücut yapıyoruz */
    [data-testid="stFileUploader"] section {
        background-color: #FDFEFE !important; /* İç bölme bembeyaz */
        border: 2px dashed #D2B4DE !important; /* Mor kesikli çizgi */
        border-radius: 15px !important;
        padding: 20px !important;
        color: #4A235A !important; /* Yazılar koyu mor */
    }

    /* "Browse files" yazan butonun siyah kalmaması için */
    [data-testid="stFileUploader"] section button {
        background-color: #E8DAEF !important;
        color: #4A235A !important;
        border: 1px solid #7D3C98 !important;
    }

    /* BUTON: Açık Lila, Büyük ve Net */
    div.stButton > button {
        background-color: #9B59B6 !important; /* Canlı bir lila */
        color: #FFFFFF !important; /* Beyaz yazı */
        border: none !important;
        border-radius: 30px !important;
        width: 100% !important;
        padding: 18px !important;
        font-weight: bold !important;
        font-size: 22px !important;
        margin-top: 20px !important;
        box-shadow: 0px 4px 15px rgba(155, 89, 182, 0.2) !important;
    }

    div.stButton > button:hover {
        background-color: #AF7AC5 !important;
        transform: scale(1.01) !important;
    }
    
    /* Yükleme sırasındaki mesajların rengi */
    .stSuccess, .stInfo, .stWarning {
        color: #4A235A !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. BAŞLIK ---
st.markdown('<div class="lilia-title">📸 Anılar Bulutta</div>', unsafe_allow_html=True)

# --- 4. TEKNİK AYARLAR ---
# Apps Script URL'ni buraya yapıştır
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
