import streamlit as st
import yt_dlp
import os
import tempfile

def download_audio(url):
    """
    Tenta baixar o áudio simulando um cliente móvel (iOS/Android), 
    que geralmente tem menos restrições de 'bot' que o cliente web.
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
        # O YouTube costuma ser mais permissivo com apps de celular
        'extractor_args': {
            'youtube': {
                'player_client': ['ios', 'android'],
                'player_skip': ['webpage', 'configs'],
            }
        },
        
        # Cabeçalhos para parecer um iPhone
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
st.markdown("Baixe suas músicas favoritas de forma simples.")

# Se o usuário quiser usar cookies de forma segura, ele pode usar as Secrets do Streamlit
# mas aqui vamos tentar sem nada primeiro.
cookies_secret = st.secrets.get("YOUTUBE_COOKIES", None)

url = st.text_input("URL do YouTube Music:", placeholder="https://music.youtube.com/watch?v=...")

if url:
    if st.button("Baixar / Download"):
        try:
            with st.spinner("Simulando acesso móvel e processando..."):
                # Se houver cookies nas secrets, usamos eles de forma invisível
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
                    st.error("Erro ao processar o arquivo.")
        except Exception as e:
            st.error(f"Erro: {str(e)}")
            st.info("Nota: O YouTube bloqueia IPs de servidores de nuvem. Se falhar, o IP do Streamlit pode estar temporariamente restrito.")

st.markdown("---")
st.caption("Segurança em primeiro lugar: Seus dados não são expostos aqui.")