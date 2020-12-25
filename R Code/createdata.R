library(stringr)
in_folder = "C:/Users/jgfri/OneDrive/Desktop/Famine Research Project/Other Data/Generated Data/temp/"

file_names = list.files(in_folder)

numbers = str_extract(file_names, "^.*[0-9]")

numbers <- numbers[order(numbers, decreasing = FALSE)]

full_file_names <- paste0(in_folder,numbers,".csv")

col_names <- c("start_year","deaths_smallpox_ratio",	"num_vaccinated_succesfully")
my_data <- data.frame(matrix(ncol = length(col_names), nrow = 0))
colnames(my_data) <- col_names

years <- sort(rep(c(1919:1928),2))
for (i in 1:length(full_file_names))
{
  if (i %% 2 != 0)
  {  
    temp_data <- read.csv(full_file_names[i])
    colnames(temp_data)[2] <- "deaths_smallpox_ratio"
  }
  else
  {
    temp_data_2 <- read.csv(full_file_names[i])
    colnames(temp_data_2)[2] <- "num_vaccinated_succesfully"
    temp_data$num_vaccinated_succesfully <- temp_data_2[colnames(temp_data_2)[2]]
    temp_data$start_year <- years[i]
    temp_data <- temp_data[,-1]
    my_data <- rbind(my_data,temp_data)
  }

  
  
}
my_data <- as.data.frame(my_data)
my_data$num_vaccinated_succesfully <- my_data$num_vaccinated_succesfully[[1]]
write.csv(my_data,"../Other Data/Generated Data/bengal_small_pox_mortality_and_vaccinated_1919-1928cleaned.csv")