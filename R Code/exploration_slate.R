library(stringr)
library(dplyr)
library(ggplot2)
library(readxl)
library(gridExtra)
mortality_df <- read_xlsx("../Other Data/mortality.xlsx")
vaccine_df_1929 <- read.csv("../Other Data/vaccination_bengal_1928_1929.csv")
vaccine_df_1928 <- read.csv("../Other Data/vaccination_bengal_1927_1928.csv")
colnames(vaccine_df_1929)[2] <- "district"
colnames(vaccine_df_1928)[2] <- "district"
vaccine_df_1929$year = 1930
vaccine_df_1928$year = 1929

my_df_1 = left_join(vaccine_df_1929,mortality_df)
my_df_2 = left_join(vaccine_df_1928,mortality_df)

g1 <- ggplot(my_df_1, aes(x=Proportion.Successfully.Vaccinated.per.1.000.surviving.population,y=infant_mortality_rate_per_thousand)) + 
  geom_point() + geom_smooth(method="lm") + xlab("Proportion of 1 year olds vaccinated") + 
  ylab("Infant Mortality Rate Per Thousand") +  ggtitle("Bengal 1930") +
  theme(plot.title = element_text(hjust = 0.5))


g2 <- ggplot(my_df_2, aes(x=Proportion.Successfully.Vaccinated.per.1.000.surviving.population,y=infant_mortality_rate_per_thousand)) + 
  geom_point() + geom_smooth(method="lm") + xlab("Proportion of 1 year olds vaccinated") + 
  ylab("Infant Mortality Rate Per Thousand") +  ggtitle("Bengal 1929") +
  theme(plot.title = element_text(hjust = 0.5))
