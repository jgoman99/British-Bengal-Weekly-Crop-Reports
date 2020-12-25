library(stringr)

filenames = list.files("../Other Data/Generated Data/district_vaccination_costs_total/")
filenames_full = paste0("../Other Data/Generated Data/district_vaccination_costs_total/",filenames)


master_data = data.frame()
for (i in 1:length(filenames_full))
{
  if (i == 1)
  {
    master_data = read.csv(filenames_full[i])
    colnames(master_data) = tolower(colnames(master_data))
  }
  else
  {
    temp_data = read.csv(filenames_full[i])
    colnames(temp_data) = tolower(colnames(temp_data))
    master_data = rbind(master_data,temp_data)
  }
}

master_data = master_data[which(!is.na(master_data$start_year)),]
master_data$rs = str_replace_all(master_data$rs,",","")
#removes Total
master_data = master_data[which(master_data$districts!="Total"),]
write.csv(master_data,"../Other Data/Generated Data/vaccination_bengal_costs.csv",row.names = FALSE)