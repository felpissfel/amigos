import streamlit as st
import requests
import os
import tempfile
import re

def get_video_id(url):
    """Extrai o ID do vídeo de uma URL do YouTube ou YouTube Music."""
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def download_via_proxy(url):
    """
    Tenta baixar o áudio usando instâncias do Invidious como proxy.
    Isso evita o bloqueio de IP direto do YouTube no Streamlit Cloud.
    """
    video_id = get_video_id(url)
    if not video_id:
        raise Exception("URL inválida. Não foi possível encontrar o ID do vídeo.")

    # Lista de instâncias públicas do Invidious estáveis
    instances = [
        "https://invidious.nerdvpn.de",
        "https://yewtu.be",
        "https://inv.nadeko.net",
        "https://invidious.flokinet.to"
    ]

    temp_dir = tempfile.gettempdir()
    
    for instance in instances:
        try:
            # 1. Obter metadados do vídeo via API do Invidious
            api_url = f"{instance}/api/v1/videos/{video_id}"
            response = requests.get(api_url, timeout=10)
            if response.status_code != 200:
                continue
            
            data = response.json()
            title = data.get('title', 'audio')
            
            # 2. Procurar pelo formato de áudio (adaptiveFormats)
            # O Invidious fornece links diretos para os streams do Google Video
            # que as instâncias costumam fazer proxy (proxy=true)
            audio_url = None
            for fmt in data.get('adaptiveFormats', []):
                if fmt.get('type', '').startswith('audio/'):
                    # Preferimos m4a ou webm que o Invidious consegue servir
                    audio_url = f"{instance}{fmt['url']}"
                    break
            
            if not audio_url:
                continue

            # 3. Baixar o arquivo de áudio
            audio_response = requests.get(audio_url, stream=True, timeout=30)
            if audio_response.status_code != 200:
                continue

            file_path = os.path.join(temp_dir, f"{video_id}.mp3")
            with open(file_path, 'wb') as f:
                for chunk in audio_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return file_path, title

        except Exception as e:
            continue # Tenta a próxima instância se houver erro
            
    raise Exception("Todas as tentativas de proxy falharam. O YouTube está bloqueando até as pontes externas no momento.")

# Interface Streamlit
st.set_page_config(page_title="YT Music Proxy Downloader", page_icon="🎧")

st.title("🎧 YT Music Downloader (Cloud Safe)")
st.markdown("""
Esta versão usa **servidores proxy (Invidious)** para contornar o bloqueio de IP do YouTube. 
Ideal para uso em nuvem e dispositivos móveis.
""")

url = st.text_input("URL do YouTube Music:", placeholder="https://music.youtube.com/watch?v=...")

if url:
    if st.button("Baixar / Download"):
        try:
            with st.spinner("Buscando áudio via proxy seguro..."):
                file_path, title = download_via_proxy(url)
                
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
            st.info("Dica: Se falhar, tente novamente em alguns segundos. As instâncias de proxy podem estar ocupadas.")

st.markdown("---")
st.caption("Solução via Proxy Invidious - Sem necessidade de cookies ou login.")