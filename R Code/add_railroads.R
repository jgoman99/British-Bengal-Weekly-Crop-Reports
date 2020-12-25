library(geosphere)
district_data <- read.csv("../Other Data/district locations.csv")
colnames(district_data)[1] <- gsub('^...','',colnames(district_data)[1])
colnames(district_data) <- tolower(colnames(district_data))
railway_data <- read.csv("../Other Data/railways_Dissolve_Simplify2_point2_until1918.csv")


min_lat <- 20
max_lat <- 28
min_lon <- 82.5
max_lon <- 92.5

get_points_within_distance <- function(data,distance,year)
{
  railway_subset_data = railway_data[which(railway_data$YEAR_OPENE<=year),]
  str_1 <- paste0("railways_within_",distance/1000,"km",year)
  str_2 <- paste0("railway_within_dummy",distance/1000,"km",year)
  data[[str_1]] <- 0
  data[[str_2]] <- 0
  for (i in 1:nrow(data))
  {
    lon <- data$long[i]
    lat <- data$lat[i]
    num <- 0
    for (j in 1:nrow(railway_subset_data))
    {
      if (distHaversine(c(lon,lat),c(railway_subset_data$POINT_X[j],railway_subset_data$POINT_Y[j])) <= distance)
      {
        num <- num + 1
      }
    }
    data[str_1][i,] <- num
    
    if(data[str_1][i,] > 0)
    {
      data[str_2] <- 1
    }
    
  }
  return(data)
}

year_range = min(railway_data$YEAR_OPENE):max(railway_data$YEAR_OPENE)
for (i in 1:length(year_range))
{
  district_data <- get_points_within_distance(district_data,5000, year_range[i])
  district_data <- get_points_within_distance(district_data,20000, year_range[i])
  district_data <- get_points_within_distance(district_data,50000, year_range[i])
}

write.csv(district_data,"../Other Data/district_with_railroads.csv",row.names = FALSE)
