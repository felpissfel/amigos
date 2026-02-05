import streamlit as st
import yt_dlp
import os
import tempfile

def download_audio(url):
    """
    Faz o download do áudio da URL fornecida e retorna o caminho do arquivo .mp3.
    """
    # Criar um diretório temporário para o download
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
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # O yt-dlp muda a extensão para .mp3 após o post-processing
        filename = ydl.prepare_filename(info)
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
                    # Opcional: remover o arquivo temporário após carregar na memória
                    # os.remove(file_path)
                else:
                    st.error("Erro ao localizar o arquivo baixado.")
        except Exception as e:
            st.error(f"Ocorreu um erro: {str(e)}")
            st.info("Dica: Verifique se a URL está correta e se o vídeo não possui restrições.")

st.markdown("---")
st.caption("Desenvolvido para uso pessoal. Respeite os direitos autorais.")
