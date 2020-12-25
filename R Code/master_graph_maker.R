library(gridExtra)
library(ggplot2)

subdata = read.csv("../Other Data/master_dataset.csv")

#add graph
plot1 <- ggplot() +
  geom_point(data=subdata[which(subdata$Districts=="Jalpaiguri"),], aes(x=start_year, y=Proportion.Successfully.Vaccinated.per.1.000.surviving.population, color = 
                                                                          "green"))
plot2 <- ggplot() +
  geom_point(data=subdata[which(subdata$Districts=="Jalpaiguri"),], aes(x=start_year, y=infant_mortality_proportion, color ="red"))


plot3 <- ggplot() +
  geom_point(data=subdata[which(subdata$Districts=="Hooghly"),], aes(x=start_year, y=Proportion.Successfully.Vaccinated.per.1.000.surviving.population, color = 
                                                                          "green"))
plot4 <- ggplot() +
  geom_point(data=subdata[which(subdata$Districts=="Hooghly"),], aes(x=start_year, y=infant_mortality_proportion, color ="red"))

plot5 <- ggplot() +
  geom_point(data=subdata[which(subdata$Districts=="Tippera"),], aes(x=start_year, y=Proportion.Successfully.Vaccinated.per.1.000.surviving.population, color = 
                                                                       "green"))
plot6 <- ggplot() +
  geom_point(data=subdata[which(subdata$Districts=="Tippera"),], aes(x=start_year, y=infant_mortality_proportion, color ="red"))

plot7 <- ggplot() +
  geom_point(data=subdata[which(subdata$Districts=="Howrah"),], aes(x=start_year, y=Proportion.Successfully.Vaccinated.per.1.000.surviving.population, color = 
                                                                       "green"))
plot8 <- ggplot() +
  geom_point(data=subdata[which(subdata$Districts=="Howrah"),], aes(x=start_year, y=infant_mortality_proportion, color ="red"))

plot9 <- ggplot() +
  geom_point(data=subdata[which(subdata$Districts=="Bankura"),], aes(x=start_year, y=Proportion.Successfully.Vaccinated.per.1.000.surviving.population, color = 
                                                                      "green"))
plot10 <- ggplot() +
  geom_point(data=subdata[which(subdata$Districts=="Bankura"),], aes(x=start_year, y=infant_mortality_proportion, color ="red"))





grid.arrange(plot1, plot2, nrow=2)
grid.arrange(plot3, plot4, nrow=2)
grid.arrange(plot5, plot6, nrow=2)
grid.arrange(plot7, plot8, nrow=2)
grid.arrange(plot9, plot10, nrow=2)