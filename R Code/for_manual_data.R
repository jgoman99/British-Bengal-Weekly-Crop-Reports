#cleans manual data for cattle data 
library(stringr)


cattle_dir <- "../Crop_Reports/Bengal Cattle Data/"

# CHANGE THISSSSS!!!!!
path_1 <- paste0(cattle_dir,"cg1930p2_folder_3.csv")
index_df = read.csv(path_1)

cattle_sheets <- list.files(cattle_dir)
cattle_sheets <- cattle_sheets[str_detect(cattle_sheets,"1930")]
for (i in 1:length(cattle_sheets))
{
  path = paste0(cattle_dir,cattle_sheets[i])
  sheet <- read.csv(path)
  if (nrow(sheet)>0)
  {
    if (sum(!is.na(sheet$District))==0)
    {
      sheet$District <- index_df$District[1:nrow(sheet)]
      #undo this comment
      if (sheet$Date=="")
      {
        print(path)
      }
      #write.csv(sheet,path, row.names = FALSE)
    }
  }

}