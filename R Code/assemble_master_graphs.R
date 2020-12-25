library(ggplot2)
library(scales)
library(readxl)

#self func
'%!in%' <- function(x,y)!('%in%'(x,y))

data <- read.csv("../Other Data/master_dataset.csv")

cross_data <- read_xlsx("../Other Data/spatial_crosswalk.xlsx")
cross_data <- as.data.frame(cross_data)

out_folder <- "../Results/Plots/automated_plots/"

# helper functions

plot_x_by_y_yearly <- function(var1,var2)
{
  name_new_folder <- paste0("plot_",var1,"_by_",var2)
  out_dir = paste0(out_folder,name_new_folder)
  if (dir.exists(out_folder))
  {
    unlink(out_dir, recursive = TRUE)
  }
  dir.create(out_dir)
  
  years <- unique(data$start_year)

  # removes years where there are not obs in x and y
  for (i in 1:length(years))
  {
    year <- years[i]
    plot_data <- data[which(data$start_year==year),]
    if (sum(plot_data[var1], na.rm = TRUE)==0)
    {
      years[i] <- NA
    }
    else if (sum(plot_data[var2], na.rm = TRUE)==0)
    {
      years[i] <- NA
    }
  

  }
  years <- years[!is.na(years)]
  
  #calculates standarization between graphs
  max_x <- max(data[var1], na.rm=TRUE)
  max_y <- max(data[var2],na.rm = TRUE)

    
  for (i in 1:length(years))
  {
    year <- years[i]

    plot_data <- data[which(data$start_year==year),]
    g <- ggplot(plot_data,aes_string(x=var1,y=var2, label = "districts")) + geom_text(size=2) + 
      scale_x_continuous(limits = c(0, max_x),labels=comma) + scale_y_continuous(limits = c(0, max_y),labels=comma)


    out_path <- paste0(out_dir,"/",year,".jpg")
    ggsave(out_path,g)

  }
}

plot_x_by_y_yearly_w_population_as_size <- function(var1,var2)
{
  name_new_folder <- paste0("plot_",var1,"_by_",var2,"_with_size")
  out_dir = paste0(out_folder,name_new_folder)
  if (dir.exists(out_folder))
  {
    unlink(out_dir, recursive = TRUE)
  }
  dir.create(out_dir)
  
  years <- unique(data$start_year)
  
  # removes years where there are not obs in x and y
  for (i in 1:length(years))
  {
    year <- years[i]
    plot_data <- data[which(data$start_year==year),]
    if (sum(plot_data[var1], na.rm = TRUE)==0)
    {
      years[i] <- NA
    }
    else if (sum(plot_data[var2], na.rm = TRUE)==0)
    {
      years[i] <- NA
    }
    
    
  }
  years <- years[!is.na(years)]
  
  #calculates standarization between graphs
  max_x <- max(data[var1], na.rm=TRUE)
  max_y <- max(data[var2],na.rm = TRUE)
  
  
  for (i in 1:length(years))
  {
    year <- years[i]
    
    plot_data <- data[which(data$start_year==year),]
    g <- ggplot(plot_data,aes_string(x=var1,y=var2, color = "districts")) + geom_point(aes(size=Population_1911_census)) + 
      scale_x_continuous(limits = c(0, max_x),labels=comma) + scale_y_continuous(limits = c(0, max_y),labels=comma)
    
    
    out_path <- paste0(out_dir,"/",year,".jpg")
    ggsave(out_path,g)
    
  }
}

plot_x_by_y_yearly <- function(var1,var2)
{
  name_new_folder <- paste0("plot_",var1,"_by_",var2)
  out_dir = paste0(out_folder,name_new_folder)
  if (dir.exists(out_folder))
  {
    unlink(out_dir, recursive = TRUE)
  }
  dir.create(out_dir)
  
  years <- unique(data$start_year)
  
  # removes years where there are not obs in x and y
  for (i in 1:length(years))
  {
    year <- years[i]
    plot_data <- data[which(data$start_year==year),]
    if (sum(plot_data[var1], na.rm = TRUE)==0)
    {
      years[i] <- NA
    }
    else if (sum(plot_data[var2], na.rm = TRUE)==0)
    {
      years[i] <- NA
    }
    
    
  }
  years <- years[!is.na(years)]
  
  #calculates standarization between graphs
  max_x <- max(data[var1], na.rm=TRUE)
  max_y <- max(data[var2],na.rm = TRUE)
  
  
  for (i in 1:length(years))
  {
    year <- years[i]
    
    plot_data <- data[which(data$start_year==year),]
    g <- ggplot(plot_data,aes_string(x=var1,y=var2, label = "districts")) + geom_text(size=2) + 
      scale_x_continuous(limits = c(0, max_x),labels=comma) + scale_y_continuous(limits = c(0, max_y),labels=comma)
    
    
    out_path <- paste0(out_dir,"/",year,".jpg")
    ggsave(out_path,g)
    
  }
}

plot_y_overtime <- function(var1)
{
  name_new_folder <- paste0("plot_",var1,"_over_time")
  out_dir = paste0(out_folder,name_new_folder)
  if (dir.exists(out_folder))
  {
    unlink(out_dir, recursive = TRUE)
  }
  dir.create(out_dir)
  
  years <- unique(data$start_year)
  
  # # removes years where there are not obs in x and y
  # for (i in 1:length(years))
  # {
  #   year <- years[i]
  #   plot_data <- data[which(data$start_year==year),]
  #   if (sum(plot_data[var1], na.rm = TRUE)==0)
  #   {
  #     years[i] <- NA
  #   }
  #   else if (sum(plot_data[var2], na.rm = TRUE)==0)
  #   {
  #     years[i] <- NA
  #   }
  #   
  #   
  # }
  #years <- years[!is.na(years)]
  
  #calculates standarization between graphs
  max_y <- max(data[var1], na.rm=TRUE)
  
  
  plot_data <- data
  g <- ggplot(plot_data,aes_string(x="start_year",y=var1)) +geom_point()
    scale_y_continuous(limits = c(0, max_y),labels=comma)
  
  
  out_path <- paste0(out_dir,"/",".jpg")
  ggsave(out_path,g)
}

plot_east_bengal_and_assam <- function(var1)
{
  name_new_folder <- paste0(var1,"_east_bengal_assam_1900to1915")
  out_dir = paste0(out_folder,name_new_folder)
  if (dir.exists(out_folder))
  {
    unlink(out_dir, recursive = TRUE)
  }
  dir.create(out_dir)
  
  ebaa_districts <- cross_data[which((cross_data$Province=="Eastern Bengal and Assam") & cross_data$Year==1905),]$District
  
  ebaa_data <- data[which((data$districts %in% ebaa_districts) & data$start_year > 1909 & data$start_year < 1915),]
  
  other_data <- data[which((data$districts %!in% ebaa_districts) & data$start_year > 1909 & data$start_year < 1915),]
  
  ggplot(data = ebaa_data, aes(x = start_year, y = total_vaccination_cost_rs))  +  
    stat_summary(fun.y = sum, geom="line", colour = "red", size = 1)
  
  ggplot(data = other_data, aes(x = start_year, y = total_vaccination_cost_rs))  +  
    stat_summary(fun.y = sum, geom="line", colour = "blue", size = 1)
  
}

# end code
# plot_x_by_y_yearly("Population_1911_census","total_vaccination_cost_rs")
# plot_x_by_y_yearly("total_vaccination_cost_rs","deaths_smallpox_ratio")
# plot_x_by_y_yearly("Population_1911_census","deaths_smallpox_ratio")
# plot_x_by_y_yearly("total_vaccination_cost_rs","Population_1911_census")
#plot_x_by_y_yearly_w_population_as_size("total_vaccination_cost_rs","deaths_smallpox_ratio")
#plot_y_overtime("deaths_smallpox_ratio")
#plot_x_by_y_yearly("Population_per_mille_1911_census","deaths_smallpox_ratio")