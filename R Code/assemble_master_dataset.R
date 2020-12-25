library(dplyr)
data <- read.csv("../Other Data/Generated Data/vaccination_and_smallpox_deaths.csv")

pop_data_1911 <- read.csv("../Other Data/Generated Data/population/population_from_1911_1912.csv")
colnames(data) <- tolower(colnames(data))
colnames(pop_data_1911)[1] <- "districts"
infant_data <- read.csv("../Other Data/Generated Data/infant_vaccination.csv")
colnames(infant_data) <- tolower(colnames(infant_data))
data <- left_join(data,infant_data , by = c("start_year","districts"))

cost_data <- read.csv("../Other Data/Generated Data/vaccination_bengal_costs.csv")
#renames column names
colnames(cost_data)[which(colnames(cost_data)=="rs")] <- "total_vaccination_cost_rs"

data <- left_join(data,cost_data)
data <- left_join(data,pop_data_1911)

#Last minute cleaning
data[which(data$districts=="Midnapur"),]$districts == "Midnapore"

# Fixes type of columns
data$total_vaccination_cost_rs <- as.numeric(data$total_vaccination_cost_rs)

write.csv(data,"../Other Data/master_dataset.csv", row.names = FALSE)