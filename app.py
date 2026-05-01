import streamlit as st
import requests
import base64

# --- 1. SAYFA AYARLARI ---
st.set_page_config(
    page_title="Lilia Event Garden | Lilia Anı Kumbarası",
    layout="centered",
    page_icon="📸"
)

# --- 2. HAFIZA YÖNETİMİ ---
if 'uploader_key' not in st.session_state:
    st.session_state['uploader_key'] = 0

if 'success_message' not in st.session_state:
    st.session_state['success_message'] = None

# --- 3. GÖRSEL TASARIM (CSS) ---
st.markdown("""
<style>
    .block-container { padding-top: 3rem !important; }
    .stApp { background-color: #FFFFFF !important; }

    .lilia-title { 
        color: #7D3C98 !important; 
        font-size: 38px !important; 
        font-weight: 700 !important; 
        text-align: center !important; 
        margin-bottom: 5px !important;
        font-family: serif !important;
    }
    
    .lilia-description {
        color: #4A235A !important;
        font-size: 18px !important;
        text-align: center !important;
        font-style: italic !important;
        margin-bottom: 30px !important;
        padding: 0 20px !important;
        line-height: 1.6 !important;
    }

    /* DOSYA SEÇME BUTONU HACK */
    [data-testid="stFileUploader"] section button span { display: none !important; }
    [data-testid="stFileUploader"] section button::after {
        content: "Hatıraları Seç" !important;
        visibility: visible !important;
        display: block !important;
    }

    [data-testid="stFileUploader"] section {
        background-color: #FDFEFE !important; 
        border: 2px dashed #D2B4DE !important; 
        border-radius: 15px !important;
    }

    /* ANA DÜĞME */
    div.stButton > button {
        background-color: #9B59B6 !important; 
        color: #FFFFFF !important; 
        border-radius: 30px !important;
        width: 100% !important;
        padding: 18px !important;
        font-weight: bold !important;
        font-size: 22px !important;
        margin-top: 10px !important;
        border: none !important;
        box-shadow: 0px 4px 15px rgba(155, 89, 182, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. BAŞLIK VE DAVET METNİ ---
st.markdown('<div class="lilia-title">📸 Lilia Anı Kumbarası</div>', unsafe_allow_html=True)

st.markdown("""
<div class="lilia-description">
    "Her kare bir hikaye anlatır. Lilia'da bu akşamın hikayesini birlikte yazmaya ne dersiniz? 
    Kendi vizörünüzden süzülen en güzel anları kumbaramıza bırakın, bu geceyi sonsuza dek ortak hafızamızda yaşatalım."
</div>
""", unsafe_allow_html=True)

# Sabit Durum Alanı
top_status_placeholder = st.empty()

if st.session_state['success_message']:
    top_status_placeholder.success(st.session_state['success_message'])
    st.session_state['success_message'] = None

# --- 5. TEKNİK AYARLAR ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw9mHDx-NZJUhzKwRLRIpvXv9hEtp_RJztM1JOF6LViPvJMGB9qjXYMPttDMl72gAI/exec"

def upload_to_drive_direct(file):
    file_bytes = file.read()
    encoded_file = base64.b64encode(file_bytes).decode("utf-8")
    payload = {
        "fileName": file.name, "mimeType": file.type, "fileData": encoded_file
    }
    response = requests.post(WEB_APP_URL, data=payload)
    return response.text

# --- 6. ARAYÜZ ---
uploaded_files = st.file_uploader(
    "Hatıraları Seç", 
    type=['png', 'jpg', 'jpeg'], 
    accept_multiple_files=True, 
    label_visibility="collapsed",
    key=f"uploader_{st.session_state['uploader_key']}"
)

if st.button("Günü Ölümsüzleştir"):
    if uploaded_files:
        with top_status_placeholder.container():
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                for i, uploaded_file in enumerate(uploaded_files):
                    status_text.info(f"Lilia Kumbarasına Ekleniyor: {i+1} / {len(uploaded_files)}")
                    upload_to_drive_direct(uploaded_file)
                    progress_bar.progress((i + 1) / len(uploaded_files))
                
                st.session_state['uploader_key'] += 1
                st.session_state['success_message'] = f"Harika! {len(uploaded_files)} yeni anı Lilia kumbarasında yerini aldı. ✨"
                st.rerun()
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
    else:
        top_status_placeholder.warning("Lütfen önce hatıraları seçin.")
