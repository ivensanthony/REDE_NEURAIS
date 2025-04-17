install.packages("shiny")

library(shiny)
library(plotly)
library(GA)

fitness_function <- function(x) {
  return(sin(x) + cos(2 * x))
}

ga_result <- ga(type = "real-valued",
                fitness = fitness_function,
                lower = -5, upper = 5,
                popSize = 30,
                maxiter = 200)

ui <- fluidPage(
  titlePanel("Visualização do Algoritmo Genético"),
  plotlyOutput("fitnessPlot")
)

server <- function(input, output) {
  output$fitnessPlot <- renderPlotly({
    x_vals <- seq(-5, 5, length.out = 1000)
    y_vals <- fitness_function(x_vals)
    
    plot_ly(x = x_vals, y = y_vals, type = 'scatter', mode = 'lines', name = 'Função Fitness') %>%
      add_markers(x = ga_result@solution, y = fitness_function(ga_result@solution), name = 'Máximo', marker = list(color = 'red', size = 10)) %>%
      layout(title = "Visualização da Função Fitness",
             xaxis = list(title = "x"),
             yaxis = list(title = "f(x)"))
  })
}

shinyApp(ui = ui, server = server)

