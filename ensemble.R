#"Ensembling relies on the assumption that different good models trained independently are likely to be good for different reasons:each model looks at slightly different aspects of the data to make its predictions, getting part of the 'truth' but not all of it".

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
data("merged")

varstring = "ROAD|pop|temp|wind|RSp|OMI|eleva|coast|I_1|Tropo"

set.seed(1)

a= sampledf(merged,fraction = 0.8, COUN,grepstring_rm = "ID|LATITUDE|LONGITUDE|ROAD_0|geometry|countryfullname" )

test = a$test
training = a$training
inde_var=a$inde_var


rf_pre = function(variabledf,  numtrees = 2000, mtry = 33, y_varname = c("day_value", "night_value", "value_mean"),   test, training, grepstring = "ROAD|pop|temp|wind|Rsp|OMI|eleva|coast", ...) {
  prenres = paste(y_varname, "|", grepstring, sep = "")
  pre_mat = subset_grep(variabledf[training, ], prenres)

  x_test = variabledf[test, ]

  formu = as.formula(paste(y_varname, "~.", sep = ""))

  rf3 <- ranger(formu, data = pre_mat, num.trees = numtrees, mtry = mtry, importance = "impurity")
  print(rf3)
  df = data.frame(imp_val = rf3$variable.importance)
  predictions(predict(rf3, data = x_test))
}


xgb_pre = function(variabledf, max_depth = 4, eta = 0.02, nthread = 2, nrounds = 300, y_varname = c("day_value", "night_value", "value_mean"), training , test ,   grepstring = "ROAD|pop|temp|wind|Rsp|OMI|eleva|coast", ...) {
  prenres = paste(y_varname, "|", grepstring, sep = "")
  sub_mat = subset_grep(variabledf, prenres)

  pre_mat = sub_mat[training, ]
  y_train = sub_mat[training, y_varname]

  x_test = sub_mat[test, ]

  df1 = data.table(pre_mat, keep.rownames = F)
  formu = as.formula(paste(y_varname, "~.", sep = ""))
  dfmatrix = sparse.model.matrix(formu, data = df1)[, -1]
  outputvec = variabledf[training, y_varname]
  bst <- xgboost(data = dfmatrix, label = outputvec, max_depth = max_depth, eta = eta, nthread = nthread, nrounds = nrounds, verbose = 0)
  print(bst)
  df_test = data.table(x_test, keep.rownames = F)
  dfmatrix_test = sparse.model.matrix(formu, data = df_test)[, -1]
  xgbpre = predict(bst, dfmatrix_test)
}

Brt_pre = function(variabledf, opti = F,  ntree = 1000, y_varname = c("day_value", "night_value", "value_mean"), training, test, grepstring = "ROAD|pop|temp|wind|Rsp|OMI|eleva|coast", ...) {
  prenres = paste(y_varname, "|", grepstring, sep = "")
  pre_mat = subset_grep(variabledf[training, ], prenres)
  x_test = variabledf[test, ]

  if (opti) {
    Xmat = subset_grep(variabledf[training, ], grepstring)
    rf3 <- gbm.step(data = pre_mat, gbm.x = names(Xmat), gbm.y = y_varname, family = "gaussian", tree.complexity = 6, learning.rate = 0.01, bag.fraction = 0.5)
    ntree = rf3$gbm.call$best.trees
  } else {
    formu = as.formula(paste(y_varname, "~.", sep = ""))
    gbm1 = gbm(formula = formu, data = pre_mat, distribution = "gaussian", n.trees = ntree, interaction.depth = 6, shrinkage = 0.01, bag.fraction = 0.5)
    print(gbm1)
    }
   predict.gbm(gbm1, x_test, n.trees = ntree, type = "response")
}

Lasso_pre = function(variabledf,  alpha = 1, y_varname = c("day_value", "night_value", "value_mean"), training, test, grepstring = "ROAD|pop|temp|wind|Rsp|OMI|eleva|coast") {
  pre_mat = subset_grep(variabledf, grepstring)
  pre_mat_tr = pre_mat[training, ]
  pre_mat_test = pre_mat[test, ]
  y_tr_value = variabledf[training, y_varname]
  y_test_value = variabledf[test, y_varname]

  cvfit <- glmnet::cv.glmnet(as.matrix(pre_mat_tr), y_tr_value, type.measure = "mse", standardize = TRUE, alpha = alpha, lower.limit = 0)
  predict(cvfit, newx = as.matrix(pre_mat_test))

}

 xgb_day= xgb_pre(inde_var, max_depth =4, eta =0.02, nthread =2, nrounds = 2000, y_varname= c("day_value"),training=training, test=test, grepstring =varstring )
 brt_day= Brt_pre(inde_var,opti = F,vis1 = F, ntree =2000,  y_varname= c("day_value"), training=training, test=test, grepstring =varstring )
 rf_day = rf_pre(inde_var, vis1 = F,y_varname= c("day_value"), training=training, test=test, grepstring =varstring)

 La_pre =  Lasso_pre(inde_var,alpha =1 , y_varname = "day_value",training=training, test=test,grepstring =varstring )

 y_test = inde_var[test,"day_value"]
 error_matrix(y_test, brt_day)
 error_matrix(y_test, rf_day)
 error_matrix(y_test, xgb_day)
 #error_matrix(y_test, La_pre) # not optimal

 ensemble = (xgb_day + brt_day+ rf_day) /3
 error_matrix(y_test, ensemble) # slightly better
