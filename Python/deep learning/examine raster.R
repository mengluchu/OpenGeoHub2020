install.packages("raster")
install.packages("rgdal")
library(raster)
for (i in 1:500)
{mapdir = paste0( "/Volumes/Seagate Expansion Drive/global/",i,"/laea/","road_class_4_25.map")
print(dim(raster(mapdir)))
}

i = 499
plot(raster(paste0( "/Volumes/Seagate Expansion Drive/global/",i,"/laea/","road_class_4_25.map")))
i = 300

plot(raster(paste0( "/Volumes/Seagate Expansion Drive/global/",i,"/laea/","road_class_4_25.map")))
 