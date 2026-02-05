import streamlit as st
import yt_dlp
import os
import tempfile

def download_audio(url):
    """
    Faz o download do áudio da URL fornecida e retorna o caminho do arquivo .mp3.
    Adiciona cabeçalhos para evitar bloqueios de 'Video Unavailable'.
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
        # Opções para evitar bloqueios de servidores/bot detection
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'no_color': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': 'https://music.youtube.com/',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Tenta extrair informações primeiro
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        # O yt-dlp muda a extensão para .mp3 após o post-processing
        mp3_filename = os.path.splitext(filename)[0] + ".mp3"
        return mp3_filename, info.get('title', 'audio')

# Configuração da página Streamlit
st.set_page_config(page_title="YouTube Music Downloader", page_icon="🎵")

st.title("🎵 YouTube Music to MP3")
st.markdown("Insira a URL do YouTube Music abaixo para baixar o áudio em formato .mp3.")

# Input da URL
url = st.text_input("URL do YouTube Music:", placeholder="https://music.youtube.com/watch?v=...")

if url:
    if st.button("Baixar / Download"):
        try:
            with st.spinner("Processando o áudio... Isso pode levar alguns segundos."):
                file_path, title = download_audio(url)
                
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.success(f"Pronto! '{title}' foi processado com sucesso.")
                        st.download_button(
                            label="Clique aqui para salvar o arquivo",
                            data=f,
                            file_name=f"{title}.mp3",
                            mime="audio/mpeg"
                        )
                else:
                    st.error("Erro ao localizar o arquivo baixado.")
        except Exception as e:
            st.error(f"Ocorreu um erro: {str(e)}")
            st.info("Dica: O YouTube às vezes bloqueia acessos de servidores de nuvem. Tente uma URL diferente ou aguarde alguns minutos.")

st.markdown("---")
st.caption("Desenvolvido para uso pessoal. Respeite os direitos autorais.")