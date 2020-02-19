library(raster)
 

dir ="/data/lu01/output_4_countries/predictors/raster/"
#dir ="/data/lu01/NWA/predictors"
lf_others = list.files(dir, full.names = T)
#dir2 ="/data/gghdc/gap/output/2019_08_nl/laea/"
#lf = list.files(dir2, pattern = "*.map$", full.names =T)
#lf  = lf[ which(grepl("road_class|indust", lf))]
#araster = raster(lf[1])
rs =stack("cNLstack")
araster = rs[[1]]
dirpre= "/data/lu01/NWA/predictors"
for (j in 1: length(lf_others)) #for each variable
{
   
   ras = raster(lf_others[j])
if (is.na(proj4string(ras)) )
  {proj4string(ras) = "+proj=longlat +datum=WGS84"} else
  {print(proj4string(ras))}

	ras = projectRaster(ras, araster)
    rr = resample(ras, araster)

    name = paste0(dirpre ,"/", names(ras), ".tif")

    writeRaster(rr, name, overwrite=TRUE )
    
  }
s1 = stack(list.files(dirpre, full.names=T))
s2 = stack(rs,s1)
writeRaster(s2, "allpredictors.grd",  overwrite =TRUE)
 #map to tif and copyfile to directory
 #for ( i in 1: length(lf))
#{
#ras = raster(lf)[i]
#name = paste0( "/data/lu01/NWA/predictors","/", names(ras), ".tif")

#writeRaster(ras, name, overwrite = T) 
#	}
