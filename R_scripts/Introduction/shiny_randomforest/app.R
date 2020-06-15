library(shiny)
library(devtools)
install_github("mengluchu/APMtools")
library(APMtools)
library(ranger)
library(raster)
library(dplyr)
library(rasterVis)
library(randomForest)
library(RColorBrewer)

# process data 
data("global_annual")
y_var = "value_mean"
prestring =  "road|nightlight|population|temp|wind|trop|indu|elev"
varstring = paste(prestring,y_var,sep="|")
inde_var = global_annual%>%merge_roads( c(3, 4, 5), keep = F)%>%na.omit() %>%ungroup()%>%dplyr::select(matches(varstring))

sr = stack("~/Documents/GitHub/OpenGeoHub2020/R_scripts/modeling_process/dc")

ui =fluidPage(
  # *Input() functions,
  # *Output() function
  sliderInput(inputId='treenum', label= "number of trees", min =1, max = 1000, value = 1, step = 20),
  sliderInput(inputId='mtry', label= "number of variables", min =2, max = 40, value = 3, step = 2),

  textOutput(outputId = "bar"),
  plotOutput(outputId = "image")
  )

server <- function(input, output){
   data = reactive({randomForest(value_mean~., inde_var, ntree = input$treenum, mtry = input$mtry )})
   
  output$bar = renderPrint({
    print(data())
    })
  
 output$image <- renderPlot({   
 a= data()
 b= predict(sr, a)
 myTheme = rasterTheme(region = rev(brewer.pal(7, "Spectral")))
 levelplot(b, at =seq(5, 50, by =3) , par.settings = myTheme)
 })
}  
 
shinyApp(ui=ui, server = server)
