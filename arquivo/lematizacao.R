library(dplyr)
sbrt_pos<-read.csv2("sbrt_dossies_sem_sentencas.csv")

texto<-filter(sbrt_pos, doc_id %in% c("40.txt", "50.txt"))

lemmaToDf<-function(texto){
  texto <- subset(texto, upos %in% c("NOUN", "ADJ", "VERB","PROPN","ADV"))
  texto$doc_id<-as.factor(texto$doc_id)
  t<-split(texto$lemma, texto$doc_id, drop = FALSE)
  t<-sapply(t, function(y){paste0(y,collapse=" ")})
  t<-tibble::enframe(t)
  names(t)<-c("doc_id","text")
  
  return(t)
  
}

txtdf<-lemmaToDf(sbrt_pos)
rm(vec)
