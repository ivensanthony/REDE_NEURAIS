install.packages("tidytext")
install.packages("dplyr")
install.packages("tidyr")  # Usado para pivot_wider()
install.packages("ggplot2")  

# Carregar os pacotes
library(tidytext)
library(dplyr)
library(tidyr)
library(ggplot2) 

# Dicionário de sentimentos em português
dicionario_sentimentos <- data.frame(
  palavra = c("feliz", "alegre", "ótimo", "incrível", "bom", "excelente", "emocionante", "maravilhoso",
              "triste", "horrível", "péssimo", "ruim", "chato", "decepcionante", "lento", "insuportável"),
  sentimento = c("positivo", "positivo", "positivo", "positivo", "positivo", "positivo", "positivo", "positivo",
                 "negativo", "negativo", "negativo", "negativo", "negativo", "negativo", "negativo", "negativo"),
  stringsAsFactors = FALSE
)

# Função para analisar sentimentos em textos
analisar_sentimentos <- function(textos) {
  df_textos <- data.frame(id = seq_along(textos), texto = textos, stringsAsFactors = FALSE)
  
  palavras_encontradas <- df_textos %>%
    unnest_tokens(palavra, texto) %>%
    inner_join(dicionario_sentimentos, by = "palavra") %>%
    count(id, sentimento)
  
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

# Textos para análise
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
print(resultados)

# Gerar e salvar o gráfico de barras
grafico <- resultados %>%
  count(sentimento) %>%
  ggplot(aes(x = sentimento, y = n, fill = sentimento)) +
  geom_bar(stat = "identity", color = "black") +
  scale_fill_manual(values = c("positivo" = "green", "negativo" = "red", "neutro" = "blue")) +
  labs(
    title = "Distribuição dos Sentimentos",
    x = "Sentimento",
    y = "Quantidade"
  ) +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    legend.position = "none"
  )

print(grafico)
ggsave("grafico_sentimentos.png", plot = grafico, width = 8, height = 6, dpi = 300)
cat("O gráfico foi salvo como 'grafico_sentimentos.png' no diretório de trabalho.\n")
getwd()
