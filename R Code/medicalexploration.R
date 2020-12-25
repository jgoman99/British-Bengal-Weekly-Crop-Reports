file_dir <- "../Other Data/Medical Data/nls-text-indiaPapers/"

file_list <- list.files(file_dir)


full_text <- ""

for (i in 1:length(file_list))
{
  print(i)
  fileName <- paste0(file_dir,file_list[i])
  full_text <- paste0(full_text,readChar(fileName, file.info(fileName)$size))
}

sink("outfile.txt")
print(full_text)
sink()