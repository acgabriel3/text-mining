library(stringr)
library(dplyr)
options(stringsAsFactors = F)
dados<-"dados/sbrt_txts/dossies"
txtdf<-readtext::readtext(dados, encoding = "latin1")
txtdf$text<-sub('.*\nConteúdo',"",txtdf$text)
txtdf$text<-sub('.*\nCONTEÚDO',"",txtdf$text)
txtdf$text<-sub('.*\nTítulo',"",txtdf$text)
txtdf$text<-gsub('[1-9][0-9]* Copyright © Serviço Brasileiro de Respostas Técnicas - SBRT - http://www.sbrt.ibict.br',"",txtdf$text)
txtdf$text<-gsub('[1-9][0-9]* Copyright © Serviço Brasileiro de Respostas Técnicas - SBRT - http://www.respostatecnica.org.br',"", txtdf$text)
txtdf$text<-gsub('[1-9][0-9]*\nCopyright © Serviço Brasileiro de Respostas Técnicas - SBRT - http://www.respostatecnica.org.br',"", txtdf$text)
txtdf$text<-gsub('\nCopyright © Serviço Brasileiro de Respostas Técnicas - SBRT - http://www.sbrt.ibict.br\n\n[1-9][0-9]*',"", txtdf$text)
txtdf$text<-gsub('Disponível em: ',"",txtdf$text)
txtdf$text<-gsub('www.+?br',"",txtdf$text)
txtdf$text<-str_replace_all(txtdf$text, "[^[:alnum:].:,?!;]", " ")
txtdf$text<-gsub("\\s+", " ", str_trim(txtdf$text))
txtdf$text<-gsub('Copyright Serviço Brasileiro de Respostas Técnicas SBRT http: www.respostatecnica.org.br [1-9][0-9]*',"",txtdf$text)
txtdf$text<-gsub('INTRODUÇÃO',"",txtdf$text)
txtdf$text<-gsub('Introdução',"",txtdf$text)
txtdf$text<- iconv(txtdf$text, from = "UTF-8", to = "ASCII//TRANSLIT")
txtdf$ID<-seq(1:nrow(txtdf))


library(udpipe)
library(data.table)
#ud_model <- udpipe_download_model(language = "portuguese")
ud_model <- udpipe_load_model("lemmatizer_model.udpipe")
x <- udpipe_annotate(ud_model, x = txtdf$text, doc_id = txtdf$ID,  parser = "none")
x <- as.data.frame(x)


# returns a data.table
annotate_splits <- function(x, file) {
  ud_model <- udpipe_load_model(file)
  x <- as.data.table(udpipe_annotate(ud_model, 
                                     x = x$text,
                                     doc_id = x$doc_id, parser = "none"))
  return(x)
}


# load parallel library future.apply
library(future.apply)

# Define cores to be used
ncores <- 4L
plan(multiprocess, workers = ncores)

# split comments based on available cores
corpus_splitted <- split(txtdf, seq(1, nrow(txtdf), by = 10))

annotation <- future_lapply(corpus_splitted, annotate_splits, file = "lemmatizer_model.udpipe")
annotation <- rbindlist(annotation)

#write.table(annotation, file="sbrt_dossies_POS.csv", sep = ";", row.names = F, fileEncoding = "utf-8")

annotation_n_sentence<- select(annotation, -sentence)

write.table(annotation_n_sentence, file="sbrt_dossies_sem_sentencas.csv", sep = ";", row.names = F, fileEncoding = "utf-8")

texto<-filter(annotation_n_sentence, doc_id=="40.txt")

texto <- subset(texto, upos %in% c("NOUN", "ADJ", "VERB","PROPN","ADV"))
vec<-(texto$lemma)

library(tm)
vectxt<-paste0(vec, collapse=" ")

