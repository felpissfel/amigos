import streamlit as st
import yt_dlp
import os
import tempfile

def download_audio(url):
    """
    Faz o download do áudio simulando um cliente móvel.
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
        'quiet': True,
        'no_warnings': True,
        
        # --- ESTRATÉGIA DE CLIENTE MÓVEL ---
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android'],
                'player_skip': ['webpage', 'configs'],
            }
        },
        
        # User-agent de iPhone para maior compatibilidade
        'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        
        'nocheckcertificate': True,
        'geo_bypass': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        mp3_filename = os.path.splitext(filename)[0] + ".mp3"
        return mp3_filename, info.get('title', 'audio')

# Interface Streamlit
st.set_page_config(page_title="YT Music Downloader", page_icon="🎵")

st.title("🎵 YouTube Music Downloader")
st.markdown("Insira a URL do YouTube Music para baixar o áudio.")

# Forma segura de verificar segredos sem causar erro
try:
    if "YOUTUBE_COOKIES" in st.secrets:
        st.sidebar.success("✅ Cookies configurados (Privado)")
except Exception:
    # Se st.secrets não estiver disponível ou o arquivo não existir, não faz nada
    pass

url = st.text_input("URL do YouTube Music:", placeholder="https://music.youtube.com/watch?v=...")

if url:
    if st.button("Baixar / Download"):
        try:
            with st.spinner("Processando áudio..."):
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
                    st.error("Erro ao localizar o arquivo.")
        except Exception as e:
            error_msg = str(e)
            st.error(f"Erro: {error_msg}")
            if "bot" in error_msg.lower() or "sign in" in error_msg.lower():
                st.warning("O YouTube bloqueou o servidor. Tente novamente em alguns minutos ou use uma URL diferente.")

st.markdown("---")
st.caption("Desenvolvido com foco em segurança e simplicidade.")