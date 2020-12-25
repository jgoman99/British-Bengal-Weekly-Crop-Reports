library(dplyr)
famine_data <- read.csv("../Crop_Reports/Bengal Cattle Data Complete/firstcleaned_tryv3.csv")
famine_data$bad_cattle <- 0
famine_data$bad_cattle[which(famine_data$cattle_result=="bad")] <- 1
famine_tbl <- as_tibble(famine_data)

sub_tbl <- famine_tbl %>%
       group_by(district) %>%
       summarize(mean_bad_cattle = mean(bad_cattle, na.rm = TRUE), latitude = unique(latitude), longitude = unique(longitude),
                 railways_within_5km = unique(railways_within_5km), railway_within_dummy5km = unique(railway_within_dummy5km),
                 railways_within_20km = unique(railways_within_20km), railway_within_dummy20km = unique(railway_within_dummy20km),
                 railways_within_50km = unique(railways_within_50km), railway_within_dummy50km = unique(railway_within_dummy50km),
                 )

# sub_tbl <- famine_tbl %>%
#   group_by(district) %>%
#   summarize(mean_bad_cattle = mean(bad_cattle, na.rm = TRUE), latitude = unique(latitude), longitude = unique(longitude),
#             railways_within_5km = unique(railways_within_5km),
#             railways_within_20km = unique(railways_within_20km),
#             railways_within_50km = unique(railways_within_50km),
#   )

fit_1 <- lm(mean_bad_cattle~railways_within_5km+railways_within_20km+railways_within_50km+latitude+longitude, sub_tbl)
fit_2 <- lm(mean_bad_cattle~railways_within_5km+latitude+longitude, sub_tbl)
fit_3 <- lm(mean_bad_cattle~railways_within_20km+latitude+longitude, sub_tbl)
fit_4 <- lm(mean_bad_cattle~railways_within_50km+latitude+longitude, sub_tbl)
fit_5 <- lm(mean_bad_cattle~railways_within_5km, sub_tbl)
fit_6 <- lm(mean_bad_cattle~railways_within_20km, sub_tbl)
fit_7 <- lm(mean_bad_cattle~railways_within_50km, sub_tbl)

sink("../Results/regressionexampleaggregate.txt")
print(summary(fit_1))
print(summary(fit_2))
print(summary(fit_3))
print(summary(fit_4))
print(summary(fit_5))
print(summary(fit_6))
print(summary(fit_7))
sink()