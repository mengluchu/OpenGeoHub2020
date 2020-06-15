library(shiny)
library(devtools)
#install_github("mengluchu/APMtools")
library(APMtools)
library(ranger)
library(raster)
library(dplyr)
library(rasterVis)
library(xgboost)
library(RColorBrewer)
library(data.table)
library(Matrix)
library(tibble)
# process data 
data("global_annual")
y_var = "value_mean"
prestring =  "road|nightlight|population|temp|wind|trop|indu|elev"
varstring = paste(prestring,y_var,sep="|")
inde_var = global_annual%>%merge_roads( c(3, 4, 5), keep = F)%>%na.omit() %>%ungroup()%>%dplyr::select(matches(varstring))

sr = raster::stack("dc")
 
ui =fluidPage(
  # *Input() functions,
  # *Output() function
  sliderInput(inputId='treenum', label= "number of trees", min =1, max = 1000, value = 1, step = 20),
  sliderInput(inputId='eta', label= "learning rate", min =0.01, max = 0.8, value = 0.8, step = 0.02),
  sliderInput(inputId='gamma', label= "penalty", min =1, max = 5, value = 1, step = 1),
  sliderInput(inputId='depth', label= "max. depth", min =1, max = 7, value = 3, step = 1),
  
  textOutput(outputId = "training"),
  tableOutput(outputId = "test"),
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
  
  output$test = renderTable({
     
 crossvali =  function(n,df, y_var) {
    smp_size <- floor(0.8 * nrow(df)) 
    set.seed(n)
    training<- sample(seq_len(nrow(df)), size = smp_size)
    test = seq_len(nrow(df))[-training] 
    P_xgb= xgboost_LUR(df, max_depth = input$depth, 
                       eta = input$eta, nthread = 4, gamma = input$gamma, nrounds = input$treenum, y_varname= y_var,training=training, test=test, grepstring =varstring)
     } 
  V2 = lapply(1:5, df = merged, y_var = y_var,crossvali)
  V2 = data.frame(five_fold_cv = rowMeans(data.frame(V2)))
  rownames_to_column(V2, var = "accu. matrix")
  })
  output$training = renderPrint({
    print(data())
  })
  
  output$image <- renderPlot({   
    a= data()
    predfun <- function(model, data) {
    v <- predict(model, as.matrix(data)) }
    b= predict(sr, a, fun = predfun)
    myTheme = rasterTheme(region = rev(brewer.pal(7, "Spectral")))
    levelplot(b, par.settings = myTheme)
  })
}  

shinyApp(ui=ui, server = server)
