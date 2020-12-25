library(geosphere)
year <- 1910
famine_data <- read.csv("../Crop_Reports/Bengal Cattle Data Complete/firstcleaned_tryv2.csv")
district_data <- read.csv("../Other Data/district locations.csv")
colnames(district_data)[1] <- gsub('^...','',colnames(district_data)[1])
colnames(district_data) <- tolower(colnames(district_data))
railway_data <- read.csv("../Other Data/railways_Dissolve_Simplify2_point2_until1918.csv")


min_lat <- 20
max_lat <- 28
min_lon <- 82.5
max_lon <- 92.5
min_year <- 1880
max_year <- 1910
railway_subset_data <- railway_data[which((railway_data$POINT_X < max_lon) & (railway_data$POINT_X > min_lon) & 
                                            (railway_data$POINT_Y < max_lat) & (railway_data$POINT_X > min_lat) &
                                            (railway_data$YEAR_OPENE >= min_year) & 
                                            (railway_data$YEAR_OPENE<= max_year)),]

get_points_within_distance <- function(data,distance)
{
  str_1 <- paste0("railways_within_",distance/1000,"km")
  str_2 <- paste0("railway_within_dummy",distance/1000,"km")
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

district_data <- get_points_within_distance(district_data,5000)
district_data <- get_points_within_distance(district_data,20000)
district_data <- get_points_within_distance(district_data,50000)

prepped_data <- left_join(famine_data,district_data)
prepped_data <- prepped_data[prepped_data$date != "",]

for (i in 1:nrow(prepped_data))
{
  row <- unlist(strsplit(prepped_data$date, "/")[i])
  
  for (j in 1:length(row))
  {
    if (nchar(row[j])< 2)
    {
      row[j] <- paste0("0",row[j])
    }
  }
  row <- paste0(row, collapse = "")
  prepped_data$date[i] <- row
}

prepped_data$date <- as.Date(prepped_data$date,"%m%d%Y")

write.csv(prepped_data,"../Crop_Reports/Bengal Cattle Data Complete/firstcleaned_tryv3.csv")