import streamlit as st
import yt_dlp
import os
import tempfile

def download_audio(url):
    """
    Tenta baixar o áudio usando o cliente 'tv', que é o mais resiliente contra bloqueios de bot.
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
        
        # --- ESTRATÉGIA DE CLIENTE TV ---
        # O cliente 'tv' (YouTube on TV) é o que menos exige desafios de bot atualmente
        'extractor_args': {
            'youtube': {
                'player_client': ['tv'],
            }
        },
        
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
st.markdown("""
Esta ferramenta tenta baixar áudios do YouTube Music. 
*Nota: Servidores de nuvem (como o Streamlit Cloud) são frequentemente bloqueados pelo YouTube.*
""")

url = st.text_input("URL do YouTube Music:", placeholder="https://music.youtube.com/watch?v=...")

if url:
    if st.button("Baixar / Download"):
        try:
            with st.spinner("Tentando bypass via protocolo de TV..."):
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
            st.error("❌ O YouTube bloqueou esta tentativa.")
            
            if "bot" in error_msg.lower() or "sign in" in error_msg.lower():
                st.warning("""
                **Por que falhou?** O YouTube identificou que este app está rodando em um servidor (Streamlit Cloud) e não em um computador pessoal.
                
                **Como resolver?**
                1. **Rodar Localmente**: Baixe este código e rode no seu PC. No seu IP residencial, ele funcionará perfeitamente.
                2. **Cookies**: A única forma de rodar na nuvem é usando cookies (o que você preferiu evitar por segurança).
                """)
                with st.expander("Ver erro técnico"):
                    st.code(error_msg)

st.markdown("---")
st.caption("Se o erro persistir, a melhor solução é a execução local.")