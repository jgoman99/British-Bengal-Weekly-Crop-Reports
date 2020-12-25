cattle_dir <- "../Crop_Reports/Bengal Cattle Data/"


file_list <- list.files(cattle_dir)

master_df <- data.frame()

x <- list()
for (i in 1:length(file_list))
{
  path <- paste0(cattle_dir,file_list[i])
  temp_df <- read.csv(path)
  
  if(sum(is.na(temp_df$District))!=0)
  {
    print(path)
    x <- append(x,path)
  }
  master_df <- rbind(temp_df,master_df)
}
x<-unlist(x)

write.csv(master_df,"../Crop_Reports/Bengal Cattle Data Complete/cattle_manual_codes.csv", row.names = FALSE)


#
# index_districts <- read.csv("../Crop_Reports/Bengal Cattle Data/cg1932p2_folder_0.csv")
# for (i in 1:length(y))
# {
#   temp_df <- read.csv(y[i])
#   
#   if (nrow(temp_df)==0)
#   {
#     
#   }
#   else if (nrow(index_districts)!=nrow(temp_df))
#   {
#     print("path wrong")
#     print(y[i])
#   }
#   else
#   {
#     temp_df$District <- index_districts$District
#     print(y[i])
#     write.csv(temp_df,y[i], row.names = FALSE)
#   }
# }

