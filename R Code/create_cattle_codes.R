library(stringr)
famine_data <- read.csv("../Crop_Reports/Bengal Crop Reports Data/main.csv")


#cleans for cattle
modified_data <- famine_data
modified_data$good_cattle <- 0
modified_data$bad_cattle <- 0
modified_data$has_cattle <- 0

modified_data$Raw_Text <- str_replace_all(modified_data$Raw_Text,"1s","is")

#modified_data$Raw_Text <- str_replace(modified_data$Raw_Text,"-", " ")
modified_data$Raw_Text <- str_replace_all(modified_data$Raw_Text,"oattle","cattle")
modified_data$Raw_Text <- str_replace_all(modified_data$Raw_Text,"cuttle","cattle")
modified_data$Raw_Text <- str_replace_all(modified_data$Raw_Text,"onttle","cattle")
modified_data$Raw_Text <- str_replace_all(modified_data$Raw_Text,"uattle","cattle")
modified_data$Raw_Text <- str_replace_all(modified_data$Raw_Text,"vattle","cattle")
modified_data$Raw_Text <- str_replace_all(modified_data$Raw_Text,"uattle","cattle")
modified_data$Raw_Text <- str_replace_all(modified_data$Raw_Text,"attle","cattle")
#quick fix
modified_data$Raw_Text <- str_replace_all(modified_data$Raw_Text,"ccattle","cattle")
modified_data$Raw_Text <- str_replace_all(modified_data$Raw_Text,"uttle","cattle")
modified_data$Raw_Text <- str_replace_all(modified_data$Raw_Text,"caittle","cattle")
modified_data$Raw_Text <- str_replace_all(modified_data$Raw_Text,"oittle","cattle")
modified_data$Raw_Text <- str_replace_all(modified_data$Raw_Text,"outtle","cattle")
modified_data$Raw_Text <- str_replace_all(modified_data$Raw_Text,"cattle","cattle")
modified_data$Raw_Text <- str_replace_all(modified_data$Raw_Text,"cattle-d\\w+","cattle-disease")

# yes. 0 means no , 1 has cattle, 2 probably has cattle
temp_index <- which(str_detect(modified_data$Raw_Text,"cattle"))
modified_data$has_cattle[temp_index] <- 1

#uses fuzzy to add ~200
modified_data$has_cattle[agrep("cattle",modified_data[which(!str_detect(modified_data$Raw_Text,"cattle")),]$Raw_Text)] <- 1

# 2 means possible
temp_index <- which(str_detect(modified_data$Raw_Text[which(modified_data$has_cattle==0)],"disease"))
modified_data$has_cattle[temp_index] <- 2
temp_index <- which(str_detect(modified_data$Raw_Text[which(modified_data$has_cattle==0)],"ttle-d"))
modified_data$has_cattle[temp_index] <- 2

add_good_cattle <- function(data,to_find)
{
  index <- which(str_detect(data$Raw_Text, to_find))
  data$good_cattle[index] <- 1
  return(data)
}
add_bad_cattle <- function(data,to_find)
{
  index <- which(str_detect(data$Raw_Text, to_find))
  data$bad_cattle[index] <- 1
  return(data)
}


# adds good cattle
modified_data[which(modified_data$has_cattle!=0),] <- add_good_cattle(modified_data[which(modified_data$has_cattle!=0),],"condition of cattle is go")
modified_data[which(modified_data$has_cattle!=0),] <- add_good_cattle(modified_data[which(modified_data$has_cattle!=0),],"no cattle-disease")
modified_data[which(modified_data$has_cattle!=0),] <- add_good_cattle(modified_data[which(modified_data$has_cattle!=0),],"no cattle")
modified_data[which(modified_data$has_cattle!=0),] <- add_good_cattle(modified_data[which(modified_data$has_cattle!=0),],"no cat")

#just adds if no exists
modified_data[which(modified_data$has_cattle!=0),][which(str_detect(modified_data[which(modified_data$has_cattle!=0),]$Raw_Text,"\\bno\\b")),]$good_cattle <- 1

#adds bad cattle
modified_data[which(modified_data$has_cattle!=0),] <- add_bad_cattle(modified_data[which(modified_data$has_cattle!=0),],"cattle disease is reported fr")
modified_data[which(modified_data$has_cattle!=0),] <- add_bad_cattle(modified_data[which(modified_data$has_cattle!=0),],"cattle-disease is reported fr")

# just adds if from and cattle disease exist (depends on matching above)
modified_data[which((modified_data$has_cattle!=0) & (modified_data$good_cattle!=1)),]$bad_cattle <- 1

# turns bad and good into bad
modified_data[which(modified_data$bad_cattle==1 & modified_data$good_cattle==1),]$good_cattle <- 0


View(modified_data[which(modified_data$has_cattle!=0),][which((modified_data[which(modified_data$has_cattle!=0),]$good_cattle == 0) & (modified_data[which(modified_data$has_cattle!=0),]$bad_cattle == 0)),])

