import streamlit as st
import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from googletrans import Translator
import matplotlib.pyplot as plt

nltk.download('vader_lexicon')

st.set_page_config(page_title="Análise de Sentimentos de Filmes", layout="centered")
st.title("🎬 Análise de Sentimentos das Avaliações de Filmes")

# Tradutor
def traduzir_texto(texto, idioma_destino='en'):
    tradutor = Translator()
    traducao = tradutor.translate(texto, dest=idioma_destino)
    return traducao.text

# Analisador
def analisar_sentimento(texto):
    texto_traduzido = traduzir_texto(texto)
    analyzer = SentimentIntensityAnalyzer()
    pontuacao = analyzer.polarity_scores(texto_traduzido)
    if pontuacao['compound'] >= 0.05:
        return 'positivo'
    elif pontuacao['compound'] <= -0.05:
        return 'negativo'
    else:
        return 'neutro'

# Processamento do DataFrame
def processar_dataframe(df):
    df['sentimento'] = df['avaliacao'].apply(analisar_sentimento)
    return df

# Upload do arquivo CSV
arquivo = st.file_uploader("Faça upload do arquivo 'avaliacoes_filmes.csv'", type=["csv"])

if arquivo:
    try:
        df = pd.read_csv(arquivo)
        
        # Verifica se as colunas corretas existem
        if 'filme' not in df.columns or 'avaliacao' not in df.columns:
            st.error("O arquivo deve conter as colunas: 'filme' e 'avaliacao'")
        else:
            st.write("Pré-visualização dos dados:")
            st.dataframe(df.head())

            if st.button("Analisar Sentimentos"):
                with st.spinner("Analisando..."):
                    df_resultado = processar_dataframe(df)
                    st.success("Análise concluída!")

                    st.write("Resultado:")
                    st.dataframe(df_resultado)

                    contagem = df_resultado['sentimento'].value_counts()
                    st.write("Distribuição dos sentimentos:")
                    st.bar_chart(contagem)

                    # Download
                    csv = df_resultado.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Baixar resultados como CSV",
                        data=csv,
                        file_name='avaliacoes_com_sentimento.csv',
                        mime='text/csv'
                    )

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
