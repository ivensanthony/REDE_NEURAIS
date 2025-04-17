import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
from googletrans import Translator
import matplotlib.pyplot as plt

# Fazendo o download dos recursos do NLTK (necessário apenas na primeira vez)
nltk.download('vader_lexicon')

def traduzir_texto(texto, idioma_destino='en'):
    """Traduz o texto para o idioma especificado (padrão: inglês)."""
    tradutor = Translator()
    traducao = tradutor.translate(texto, dest=idioma_destino)
    return traducao.text

def analisar_sentimento(texto):
    """Analisa o sentimento de um texto e retorna a polaridade."""
    texto_traduzido = traduzir_texto(texto)  # Traduzindo o texto para inglês
    analyzer = SentimentIntensityAnalyzer()
    pontuacao = analyzer.polarity_scores(texto_traduzido)
    if pontuacao['compound'] >= 0.05:
        return 'positivo'
    elif pontuacao['compound'] <= -0.05:
        return 'negativo'
    else:
        return 'neutro'

def analisar_sentimentos_dataframe(dataframe, coluna_texto):
    """Analisa os sentimentos de um dataframe e adiciona uma coluna com a polaridade."""
    dataframe['sentimento'] = dataframe[coluna_texto].apply(analisar_sentimento)
    return dataframe

def gerar_grafico_sentimentos(dataframe):
    """Gera um gráfico de barras com a contagem de cada sentimento."""
    contagem_sentimentos = dataframe['sentimento'].value_counts()
    contagem_sentimentos.plot(kind='bar', color=['green', 'red', 'blue'])
    plt.title('Distribuição dos Sentimentos')
    plt.xlabel('Sentimentos')
    plt.ylabel('Frequência')
    plt.xticks(rotation=0)
    plt.show()

# Exemplo de uso com um DataFrame do pandas
texto = {
    'texto': [
        "Adorei o produto, superou minhas expectativas!",
        "O serviço foi péssimo, não recomendo.",
        "É um produto ok, nada de especial.",
        "Estou muito feliz com a compra!",
        "Que decepção, perdi meu dinheiro."
    ]
}
df = pd.DataFrame(texto)
df_com_sentimentos = analisar_sentimentos_dataframe(df, 'texto')
print(df_com_sentimentos)
gerar_grafico_sentimentos(df_com_sentimentos)
