
xgbname = "xgbnij.tif"
rfname = "rfmnij.tif"
laname = "Lamnij.tif"

ipak <- function(pkg){

  new.pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
  if (length(new.pkg))
    install.packages(new.pkg, dependencies = TRUE, repos='http://cran.muenster.r-project.org')
  sapply(pkg, require, character.only = TRUE)
}
packages <- c( "raster", "dplyr", "devtools", "rgdal","Matrix","xgboost", "data.table" , "randomForest", "glmnet"    )
ipak(packages)
install_github("mengluchu/APMtools")
library(APMtools)
sr =  stack("plot3methods/allpredictors")

#use this to merge roads if needed: sr[[names(sr)[grepl("road_class",names(sr))]]]
sr3 = sr[[names(sr)[grepl("road_class_3_",names(sr))]]]
sr4 = sr[[names(sr)[grepl("road_class_4_",names(sr))]]]
sr5 = sr[[names(sr)[grepl("road_class_5_",names(sr))]]]
sr6 = sr[[names(sr)[grepl("road_class_1_|road_class_2_|temp|indu|wind|trop|Rsp|pop|OMI",names(sr))]]]
sr345 =sr3+sr4+sr5
srmerged  = stack(sr345,sr6)

data(merged)
merged = merged%>% na_if( -1)%>%na.omit
a= sampledf(merged,fraction = 1, country2digit = 'World') #for world
inde_var = a$inde_var
inde_var = merge_roads(inde_var, c(3, 4, 5), keep = F)

names(inde_var) =  gsub("M345", "3", names(inde_var)) # note 3 is for M345

names(inde_var) = gsub("ROAD_", "road_class_", names(inde_var))
names(inde_var) = gsub("I_1", "industry", names(inde_var))
names(inde_var) = gsub("Tropomi_2018", "trop_mean_filt", names(inde_var))
names(inde_var) = gsub("RSp", "Rsp", names(inde_var))

 
predicLA_RF_XGBtiles(df = inde_var, rasstack = srmerged, yname = "value_mean", varstring = "road|temperature|wind|pop|ele|Rsp|rop|OMI|industry", xgbname=xgbname, rfname = rfname, laname = laname, ntree = 1000,   max_depth = 6, eta = 0.02, nthread = 4, nrounds = 1000 )
