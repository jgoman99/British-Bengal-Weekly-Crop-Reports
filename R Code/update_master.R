library(stringr)
library(geosphere)
library(dplyr)
library(gridExtra)
library(ggplot2)

generated_dir = "../Other Data/Generated Data/"
vaccine_filenames = list.files(generated_dir)

master_df = data.frame()
for (i in 1:length(vaccine_filenames))
{
  path = paste0(generated_dir,vaccine_filenames[i])
  

  data = read.csv(path)
  
  if (sum(colnames(data)=="image") < 1)
  {
    data$image = "Exists"
  }
  #quick fix
  if (i != 1)
  {
    colnames(data) = colnames(master_df)
  }

  master_df = rbind(master_df,data)
}

#sets up year
master_df$start_year = str_extract(master_df$year,"[0-9]{4}")

#gets railroads by year
district_location_data <- read.csv("../Other Data/district locations.csv")
colnames(district_location_data)[1] <- gsub('^...','',colnames(district_location_data)[1])
colnames(district_location_data) <- tolower(colnames(district_location_data))
railway_data <- read.csv("../Other Data/railways_Dissolve_Simplify2_point2_until1918.csv")


get_railroads <- function(lat,lon,distance,year)
{
  railway_subset_data = railway_data[which(railway_data$YEAR_OPENE<=year),]
  
  num <-0
  for (j in 1:nrow(railway_subset_data))
  {
    if (distHaversine(c(lon,lat),c(railway_subset_data$POINT_X[j],railway_subset_data$POINT_Y[j])) <= distance)
    {
      num <- num + 1
    }
  }
  return(num)
}

#cleans districts
master_df$Districts = str_replace_all(master_df$Districts,"\\.\\.\\.","")
master_df$Districts = str_replace_all(master_df$Districts,"-"," ")

master_df = left_join(master_df,district_location_data, by = c("Districts"="district"))
master_df_no_na = master_df[which(!is.na(master_df$lat)),]
master_df_no_na$railways_within_20km = NA
master_df_no_na$railways_within_50km = NA
for (i in 1:nrow(master_df_no_na))
{
  total_length = nrow(master_df_no_na)
  print(paste0(i,"/",total_length, "completed"))
  row = master_df_no_na[i,]
  lat = row$lat
  lon = row$long
  year = row$start_year
  
  row$railways_within_20km = get_railroads(lat,lon,20000,year)
  row$railways_within_50km = get_railroads(lat,lon,50000,year)
  
  master_df_no_na[i,] <- row
  
}

dataV1 = master_df_no_na
numerify_colnames = colnames(dataV1)
numerify_colnames = numerify_colnames[numerify_colnames!="Districts"]
numerify_colnames = numerify_colnames[numerify_colnames!="image"]
numerify_colnames = numerify_colnames[numerify_colnames!="year"]
# removes commas from entire dataframe
for (i in 1:length(numerify_colnames))
{
  
  dataV1[numerify_colnames[i][[1]]] = as.numeric(gsub(",","",dataV1[numerify_colnames[i]][[1]]))
}

dataV2 = dataV1
dataV2$railways_within_50km_proportion <- dataV2$railways_within_50km/dataV2$Population.among.which.vaccinations.were.performed
dataV2$infant_mortality_proportion <- dataV2$Mortality.infants.under.one.year/dataV2$Population.among.which.vaccinations.were.performed

#remove problem
dataV2 = dataV2[which(dataV2$Districts!="Nadia" & dataV2$start_year!="1910"),]

data_final = dataV2
write.csv(data_final,"../Other Data/master_dataset.csv", row.names = FALSE)