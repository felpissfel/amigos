import streamlit as st
import yt_dlp
import os
import tempfile

def download_audio(url):
    """
    Faz o download do áudio usando OAuth2 para autenticação oficial.
    """
    temp_dir = tempfile.gettempdir()
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'quiet': False, # Deixamos False para capturar mensagens de log se necessário
        'no_warnings': False,
        
        # --- AUTENTICAÇÃO OAUTH2 ---
        # Isso fará o YouTube tratar o app como uma "Smart TV" ou app autorizado
        'username': 'oauth2',
        'password': '', 
        
        # Opções extras de estabilidade
        'nocheckcertificate': True,
        'geo_bypass': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        mp3_filename = os.path.splitext(filename)[0] + ".mp3"
        return mp3_filename, info.get('title', 'audio')

# Interface Streamlit
st.set_page_config(page_title="YT Music Downloader (OAuth)", page_icon="🎵")

st.title("🎵 YouTube Music Downloader")
st.markdown("""
### ⚠️ Instrução de Primeiro Acesso:
O YouTube exige que você confirme que não é um robô. 
1. Clique em **Baixar**.
2. Se for a primeira vez, o app pode travar ou mostrar uma mensagem pedindo para você autorizar.
3. Verifique os logs do Streamlit (ou o terminal) para um link como `https://www.google.com/device` e um código.
4. Acesse o link, cole o código e autorize com sua conta Google.
""")

url = st.text_input("URL do YouTube Music:", placeholder="https://music.youtube.com/watch?v=...")

if url:
    if st.button("Baixar / Download"):
        try:
            with st.spinner("Autenticando e processando..."):
                file_path, title = download_audio(url)
                
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.success(f"Sucesso! '{title}' pronto.")
                        st.download_button(
                            label="📥 Baixar MP3",
                            data=f,
                            file_name=f"{title}.mp3",
                            mime="audio/mpeg"
                        )
                else:
                    st.error("Arquivo não encontrado.")
        except Exception as e:
            error_msg = str(e)
            if "To sign in, use a web browser to open the page" in error_msg or "code" in error_msg.lower():
                st.warning("🔑 **Ação Necessária:** Verifique os logs do seu servidor/Streamlit Cloud. Você verá um código de autenticação do Google. Siga as instruções lá para autorizar o acesso.")
                st.code(error_msg) # Tenta mostrar o erro/instrução diretamente na tela
            else:
                st.error(f"Erro: {error_msg}")

st.markdown("---")
st.caption("Versão com Autenticação OAuth2")