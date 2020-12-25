library(ggplot2)
library(gridExtra)
library(dplyr)

out_path = "C:/Users/jgfri/OneDrive/Desktop/Famine Research Project/Results/Plots/vaccination_and_smallpox_master_with_child_vax/"

data <- read.csv("../Other Data/Generated Data/vaccination_and_smallpox_deaths.csv")
pop_data <- read.csv("../Other Data/district locations.csv")
colnames(data) <- tolower(colnames(data))
colnames(pop_data)[1] <- "districts"
infant_data <- read.csv("../Other Data/Generated Data/infant_vaccination.csv")
colnames(infant_data) <- tolower(colnames(infant_data))
data <- left_join(data,infant_data , by = c("start_year","districts"))
districts = unique(data$districts)

for (i in 1:length(districts))
{
  district = districts[i]
  pop <- pop_data[pop_data$districts==district,]$Population_1921
  filename = paste0(out_path,district,pop,".jpg")
  
  temp_data <- data[which(data$districts==district),]
  
  g1 <- ggplot(temp_data) + geom_line(aes(x=start_year,y=num_vaccinated_succesfully)) + xlab("Year") + ylab("Num. Suc. Vacc.")
  g2 <- ggplot(temp_data) + geom_line(aes(x=start_year,y=deaths_smallpox_ratio)) + xlab("Year") + ylab("Smallpox deaths per 1000")
  g3 <- ggplot(temp_data) + geom_line(aes(x=start_year,y=number.succesfully.vaccinated)) +
    xlab("Year") +ylab("Num inf. vacc.")
  
  
  g3<- grid.arrange(g3,g1,g2,nrow=3)
  ggsave(file=filename, g3)
}



