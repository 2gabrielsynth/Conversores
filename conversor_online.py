import streamlit as st
from gtts import gTTS
import PyPDF2 as lpdf

def ler_pdf(file):
    try:
        ler_pdf = lpdf.PdfFileReader(file)

        if ler_pdf.numPages > 0:
            extrai_texto = ''

            for num_pagina in range(ler_pdf.numPages):
                pagina = ler_pdf.getPage(num_pagina)
                extrai_texto += pagina.extractText()
            return extrai_texto
        else:
            return "Arquivo inválido ou sem páginas"

    except Exception as e:
        return f"Erro: {str(e)}"

def converter_texto_audio(texto, nomedoarquivo):
    audio_path = f"{nomedoarquivo}.mp3"
    tts = gTTS(text=texto, lang='pt-br')
    tts.save(audio_path)
    return audio_path

with st.container():
    st.write("Converta Texto para Áudio")

    texto = st.text_input("Digite algo:")
    nomedoarquivo = st.text_input("Digite o nome do arquivo:")

    if st.button("Converter para Áudio"):
        if nomedoarquivo:
            audio_file_path = converter_texto_audio(texto, nomedoarquivo)

            with open(audio_file_path, "rb") as file:
                file_content = file.read()
                st.download_button(label="Baixar áudio", data=file_content, file_name=f"{nomedoarquivo}.mp3", key=None, help=None)
                print(f"Usuário salvou com o nome do {nomedoarquivo}")
        else:
            st.warning("Digite um nome de arquivo antes de converter.")

with st.container():
    st.write("Converta PDF para Texto")

    uploaded_file = st.file_uploader("Faça upload de um arquivo PDF", type=["pdf"])

    if uploaded_file:
        nomedoarquivo2 = st.text_input("Digite o nome do arquivo PDF:")
        if st.button("Converter para Texto"):
            if nomedoarquivo2:
                pdf_text = ler_pdf(uploaded_file)

                with st.expander("Texto extraído do PDF"):
                    st.text(pdf_text)
            else:
                st.warning("Digite um nome de arquivo antes de converter.")
