library(shiny)
library(devtools)
install_github("mengluchu/APMtools")
library(APMtools)
library(ranger)
library(raster)
library(dplyr)
library(rasterVis)
library(xgboost)
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
  sliderInput(inputId='eta', label= "learning rate", min =0.01, max = 0.8, value = 0.8, step = 0.02),
  sliderInput(inputId='gamma', label= "penalty", min =1, max = 5, value = 1, step = 1),
  sliderInput(inputId='depth', label= "max. depth", min =1, max = 7, value = 3, step = 1),
  
  textOutput(outputId = "bar"),
  plotOutput(outputId = "image")
)

server <- function(input, output){
  data = reactive({
    re = names(sr)
    pre_mat3 = inde_var %>% dplyr::select(re)
    stopifnot(all.equal(names(sr), names(pre_mat3)))
    pre_mat3 = na.omit(pre_mat3)
    yvar = inde_var%>% dplyr::select(y_var) %>% unlist()
    indep_dep = data.frame(yvar = yvar, pre_mat3)
    df1 = data.table(indep_dep, keep.rownames = F)
    formu = as.formula(paste("yvar", "~.", sep = ""))
    dfmatrix = sparse.model.matrix(formu, data = df1)[, -1]
    bst <- xgboost(data = dfmatrix, label = yvar, max_depth = input$depth, 
                                  eta = input$eta, nthread = 4, gamma = input$gamma, nrounds = input$treenum, 
                                  verbose = 0)})
  
  output$bar = renderPrint({
    print(data())
  })
  
  output$image <- renderPlot({   
    a= data()
    predfun <- function(model, data) {
      v <- predict(model, as.matrix(data))
    }
    b= predict(sr, a, fun = predfun)
    myTheme = rasterTheme(region = rev(brewer.pal(7, "Spectral")))
    levelplot(b, par.settings = myTheme)
  })
}  

shinyApp(ui=ui, server = server)
