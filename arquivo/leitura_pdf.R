library(pdftools)
pdf1<-"/home/micael/R_envs/text-mining/dados/sbrt_txts/respostas/34639.txt"
toc <- pdf_toc(pdf1)

# Show as JSON
jsonlite::toJSON(toc, auto_unbox = TRUE, pretty = TRUE)

info<-pdf_text(pdf1)
