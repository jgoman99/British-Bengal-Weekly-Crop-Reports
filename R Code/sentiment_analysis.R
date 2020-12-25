#remember to cite nrc
#have to convert wors like damaged to damage
library(tidytext)
library(dplyr)
library(stringr)

famine_data <- read.csv("../Crop_Reports/Bengal Crop Reports Data/main.csv")
famine_data <- as_tibble(famine_data)
famine_data$Raw_Text <- str_replace_all(famine_data$Raw_Text, "\\.", "")
famine_data$Raw_Text <- str_replace_all(famine_data$Raw_Text, "-", "")
famine_data$num_negative <- numeric(length=nrow(famine_data))
famine_data$num_positive <- numeric(length=nrow(famine_data))

# NRC Lexicon
nrc_positive <- get_sentiments("nrc") %>% 
  filter(sentiment == "positive")

nrc_negative <- get_sentiments("nrc") %>% 
  filter(sentiment == "negative")


for (i in 1:nrow(famine_data))
{
  num_negative <- 0
  num_positive <- 0
  print(paste0("current i:",i))
  text_str = unlist(strsplit(famine_data[i,]$cleaned_text," "))
  text_tib <- tibble("test", text_str)
  colnames(text_tib) <- c("test", "word")
  
  positive_tib <- text_tib %>%
    inner_join(nrc_positive) %>%
    count(word,sort = TRUE)
  
  negative_tib <- text_tib %>%
    inner_join(nrc_negative) %>%
    count(word,sort = TRUE)
  
  if (nrow(positive_tib) > 0)
  {
    num_positive <- positive_tib %>% select(n) %>% sum
  }
  if (nrow(negative_tib) > 0)
  {
    num_negative <- negative_tib %>% select(n) %>% sum
  }
  

  
  famine_data[i,]$num_negative <- num_negative
  famine_data[i,]$num_positive <- num_positive
  
  
}

write.csv(famine_data,"../Crop_Reports/Bengal Crop Reports Data/main.csv", row.names = FALSE)

# negative is usually longer. use negative. (bc positive comes from when bad things happenng e.g. not favorable)





