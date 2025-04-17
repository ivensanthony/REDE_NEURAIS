# Instalar os pacotes (roda só uma vez)
install.packages("tidytext")
install.packages("dplyr")
install.packages("tidyr")  # Usado para pivot_wider()
install.packages("ggplot2")  # Instalar o pacote ggplot2 (se ainda não estiver instalado)

# Carregar os pacotes
library(tidytext)
library(dplyr)
library(tidyr)
library(ggplot2)  # Carregar o pacote ggplot2

# Dicionário de sentimentos em português
dicionario_sentimentos <- data.frame(
  palavra = c("feliz", "alegre", "ótimo", "incrível", "bom", "excelente", "emocionante", "maravilhoso",
              "triste", "horrível", "péssimo", "ruim", "chato", "decepcionante", "lento", "insuportável"),
  sentimento = c("positivo", "positivo", "positivo", "positivo", "positivo", "positivo", "positivo", "positivo",
                 "negativo", "negativo", "negativo", "negativo", "negativo", "negativo", "negativo", "negativo"),
  stringsAsFactors = FALSE
)

# Função para analisar vários textos de uma vez
analisar_sentimentos <- function(textos) {
  # Cria um data frame com os textos
  df_textos <- data.frame(id = seq_along(textos), texto = textos, stringsAsFactors = FALSE)
  
  # Quebra os textos em palavras (tokenização)
  palavras_encontradas <- df_textos %>%
    unnest_tokens(palavra, texto) %>%
    inner_join(dicionario_sentimentos, by = "palavra") %>%
    count(id, sentimento)
  
  # Junta as contagens com os textos originais
  resultados <- df_textos %>%
    left_join(palavras_encontradas %>%
                pivot_wider(names_from = sentimento, values_from = n, values_fill = 0),
              by = "id") %>%
    mutate(
      positivo = ifelse(is.na(positivo), 0, positivo),
      negativo = ifelse(is.na(negativo), 0, negativo),
      sentimento = case_when(
        positivo > negativo ~ "positivo",
        negativo > positivo ~ "negativo",
        TRUE ~ "neutro"
      )
    ) %>%
    select(texto, sentimento)
  
  return(resultados)
}

# Exemplo de uso com vários textos
textos <- c(
  "Estou muito feliz com o resultado, foi ótimo!",
  "Que dia horrível, tudo deu errado.",
  "A comida estava boa, mas o atendimento foi ruim.",
  "Não sei o que sentir sobre isso.",
  "Um filme excelente e emocionante!",
  "O atendimento foi péssimo, mas o produto era bom.",
  "Tudo aconteceu de forma maravilhosa, estou alegre.",
  "O filme foi chato e muito lento."
)

# Executar a análise
resultados <- analisar_sentimentos(textos)

# Ver os resultados
print(resultados)

# Gerar um gráfico de barras para visualizar os sentimentos
grafico <- resultados %>%
  count(sentimento) %>%
  ggplot(aes(x = sentimento, y = n, fill = sentimento)) +
  geom_bar(stat = "identity") +
  labs(
    title = "Distribuição dos Sentimentos",
    x = "Sentimento",
    y = "Quantidade"
  ) +
  theme_minimal()

# Exibir o gráfico
print(grafico)
