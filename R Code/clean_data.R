library(hunspell)
library(beepr)


famine_data <- read.csv("../Crop_Reports/Bengal Crop Reports Data/main.csv")
famine_data$cleaned_text <- ""

naive_cleaning <- function(text_str){
  stripped_text_str <- strip(text_str)
  text_vec <- unlist(strsplit(stripped_text_str, " "))
  text_vec[!hunspell_check(text_vec)] <- sapply(text_vec[!hunspell_check(text_vec)], naive_suggest)
  
  cleaned_text <- paste(text_vec, collapse = " ")
  return(cleaned_text)
  
}

naive_suggest <- function(word_str)
{
  suggested_word <- hunspell_suggest(word_str)[[1]][1]
  
  return(suggested_word)
}

famine_data$cleaned_text <- sapply(famine_data$Raw_Text,naive_cleaning)

write.csv(famine_data,"../Crop_Reports/Bengal Crop Reports Data/main.csv")

beep(3)