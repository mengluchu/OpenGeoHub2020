
######################################################################
# differences between classical statistics and machine learning
### ###################################################################

COUN="world"

ipak <- function(pkg){

  new.pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
  if (length(new.pkg))
    install.packages(new.pkg, dependencies = TRUE, repos='http://cran.muenster.r-project.org')
  sapply(pkg, require, character.only = TRUE)
}
packages <- c( "sp","maptools", "MASS" ,"raster", "sf","dplyr", "glmnet","ggplot2" ,"reshape2","lme4" , "tidyr", "RColorBrewer","devtools", "rasterVis","corrplot", "randomForest", "forestFloor","ranger","forecast"  ,"party","dismo","gbm","data.table","xgboost","vcd","Matrix")
ipak(packages)

install_github("mengluchu/APMtools")
library(APMtools)
ls("package:APMtools")
data("merged")
varstring = "ROAD|pop|temp|wind|RSp|OMI|eleva|coast|I_1|Tropo"

set.seed(1)

a= sampledf(merged,fraction = 0.8, COUN,grepstring_rm = "ID|LATITUDE|LONGITUDE|ROAD_0|geometry|countryfullname" )

test = a$test
training = a$training
inde_var=a$inde_var
y_train = inde_var[training,"day_value"]
# predict
xgb_day= xgb_pre(inde_var, max_depth =4, eta =0.02, nthread =4, nrounds = 1000, y_varname= c("day_value"),training=training, test=training, grepstring =varstring )
#brt_day= Brt_pre(inde_var,opti = F, ntree =1000,  y_varname= c("day_value"), training=training, test=training, grepstring =varstring )
#rf_day = rf_pre(inde_var, y_varname= c("day_value"), training=training, test=training , grepstring =varstring)
La_pre =  Lasso_pre(inde_var,alpha =1 , y_varname = "day_value",training=training, test=training ,grepstring =varstring )

# training and test on the same dataset:
error_matrix(y_train,La_pre)
error_matrix(y_train,xgb_day)

#df =data.frame(y_train, xgb_day = xgb_day, brt_day=brt_day,rf_day=rf_day, La_day = La_pre )
#plot(df)

#summary(lm(y_train~., data = df))
#coef(lm(y_train~., data = df))

