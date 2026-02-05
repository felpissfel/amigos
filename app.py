import streamlit as st
import yt_dlp
import os
import tempfile
import random

def download_audio(url):
    """
    Faz o download do áudio com técnicas avançadas para evitar detecção de bot.
    """
    temp_dir = tempfile.gettempdir()
    
    # Lista de User-Agents modernos para rotacionar ou usar um fixo robusto
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    ]

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
        
        # --- ESTRATÉGIAS DE EVASÃO ---
        'user_agent': random.choice(user_agents),
        'referer': 'https://www.google.com/', # Simula vindo de uma busca
        'nocheckcertificate': True,
        'geo_bypass': True,
        'add_header': [
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language: pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Upgrade-Insecure-Requests: 1',
        ],
        # Força o uso de IPv4, pois IPv6 de data centers é bloqueado mais facilmente
        'source_address': '0.0.0.0', 
        # Tenta usar o extrator do Android que às vezes tem menos restrições
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web'],
                'skip': ['dash', 'hls']
            }
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        mp3_filename = os.path.splitext(filename)[0] + ".mp3"
        return mp3_filename, info.get('title', 'audio')

# Interface Streamlit
st.set_page_config(page_title="YT Music Downloader PRO", page_icon="🎧")

st.title("🎧 YouTube Music Downloader")
st.info("Nota: Se houver erro de 'Bot', tente clicar no botão novamente após alguns segundos.")

url = st.text_input("Cole a URL do YouTube Music:", placeholder="https://music.youtube.com/watch?v=...")

if url:
    if st.button("Baixar / Download"):
        try:
            with st.spinner("Simulando acesso e processando áudio..."):
                file_path, title = download_audio(url)
                
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.success(f"Sucesso! '{title}' pronto para download.")
                        st.download_button(
                            label="📥 Salvar MP3",
                            data=f,
                            file_name=f"{title}.mp3",
                            mime="audio/mpeg"
                        )
                else:
                    st.error("Arquivo não encontrado após o processamento.")
        except Exception as e:
            error_msg = str(e)
            if "confirm you're not a bot" in error_msg:
                st.error("O YouTube detectou o servidor como um bot. 🤖")
                st.warning("Dica: Tente clicar no botão novamente. Às vezes, a rotação de identidade funciona na segunda tentativa.")
            else:
                st.error(f"Erro: {error_msg}")

st.markdown("---")
st.caption("Ferramenta de conversão para fins educacionais.")