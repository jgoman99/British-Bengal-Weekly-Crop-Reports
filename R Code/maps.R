library("ggplot2")
theme_set(theme_bw())
library("sf")
library("rnaturalearth")
library("rnaturalearthdata")
library("rgeos")

# Loads railway data
railway_data <- read.csv("../Other Data/railways_Dissolve_Simplify2_point2_until1918.csv")
district_data <- read.csv("../Other Data/district locations.csv", header = TRUE)
famine_data <- read.csv("../Crop_Reports/Bengal Crop Reports Data/main.csv")
colnames(district_data) <- c("district","latitude","longitude")

world <- ne_countries(scale = "medium", returnclass = "sf")


sites <- data.frame(longitude = c(district_data$longitude), latitude = c(district_data$latitude))
sites <- st_as_sf(sites, coords = c("longitude", "latitude"), 
                  crs = 4326, agr = "constant")

min_lat <- 20
max_lat <- 28
min_lon <- 82.5
max_lon <- 92.5
min_year <- 1880
max_year <- 1900
railway_subset_data <- railway_data[which((railway_data$POINT_X < max_lon) & (railway_data$POINT_X > min_lon) & 
                                            (railway_data$POINT_Y < max_lat) & (railway_data$POINT_X > min_lat) &
                                            (railway_data$YEAR_OPENE >= min_year) & 
                                            (railway_data$YEAR_OPENE<= max_year)),]
# railways <- data.frame(longitude = c(railway_subset_data$POINT_X), 
#                        latitude = c(railway_subset_data$POINT_Y), railway_id = c(railway_subset_data$InLine_FID))
# railways <- st_as_sf(railways, coords = c("longitude", "latitude"), 
#                   crs = 4326, agr = "constant")

#lat lon <u,v> may be off
ggplot(data = world) +
  geom_sf() +
  geom_sf(data = sites, size = 4, shape = 23, fill = "darkred") +
  geom_point(data = railway_subset_data, aes(x=POINT_X,y= POINT_Y, color = as.character(InLine_FID))) +
  #geom_sf(data = railways, size = 4, shape = 20) +
  coord_sf(xlim = c(min_lon, max_lon), ylim = c(min_lat,max_lat), expand = FALSE) +
  ggtitle(paste0("Districts & Railways in India: ", min_year, "-", max_year)) +
  theme(legend.position = "none")