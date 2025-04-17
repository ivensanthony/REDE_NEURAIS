library(neuralnet)
library(ggplot2)

# Criar dados de entrada
set.seed(123)
data <- data.frame(
  x1 = runif(100, 0, 1),
  x2 = runif(100, 0, 1),
  y = as.integer(runif(100, 0, 1) > 0.5)
)

# Treinar a rede neural
net <- neuralnet(y ~ x1 + x2, data, hidden = 3, linear.output = FALSE)

# Visualizar a rede neural
plot(net, rep = "best")

# Visualizar os dados de entrada e a saída previstaA
pred <- compute(net, data[, c("x1", "x2")])$net.result
data$predicted <- ifelse(pred > 0.5, 1, 0)

ggplot(data, aes(x = x1, y = x2, color = as.factor(predicted))) +
  geom_point(size = 3) +
  labs(title = "Visualização dos Dados e Previsões da Rede Neural",
       x = "x1", y = "x2", color = "Previsão") +
  theme_minimal()