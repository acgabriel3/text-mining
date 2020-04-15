library(udpipe)
library(dplyr)


#Faz o download e carrega o modelo.
ud_model <- udpipe_download_model(language = "portuguese")
ud_model <- udpipe_load_model(ud_model$file_model)


lemmaToDf<-function(txtdf){
  txtdf<-select(txtdf, doc_id, text)
  names(txtdf)<-c("doc_id", "text")
  texto <- udpipe_annotate(ud_model, x = txtdf$text, doc_id = txtdf$doc_id,parser = "none")
  texto <- as.data.frame(texto)
  texto <- subset(texto, upos %in% c("NOUN", "ADJ", "VERB","PROPN","ADV"))
  texto$doc_id<-as.factor(texto$doc_id)
  t<-split(texto$lemma, texto$doc_id, drop = FALSE)
  t<-sapply(t, function(y){paste0(y,collapse=" ")})
  t<-tibble::enframe(t)
  names(t)<-c("doc_id","text")
  
  return(t)
  
}


export.doc.lemmatized <- function(txtdf, dir_saida=NULL) {
  
  for(i in 1:length(txtdf$doc_id)){
    txt<-lemmaToDf(txtdf[i,1:2])
    file_name<-paste0(txt$doc_id,".txt")
    write(txt$text, file = paste0(dir_saida,file_name))
    cat("Exportando arquivo",i, "de", length(txtdf$doc_id), "arquivos.", "\n")
    cat("Arquivo", file_name, "salvo no diretório:", dir_saida, "\n")
  }
  
}


dossies_dir<-"dados/sbrt_txts/dossies"
metadados_dir<-"dados/sbrt_dossies_metadados.json"


#Leitura e pré-processamento dos documentos.
txtdf<-get_txt(dossies_dir,metadados_dir)

export.doc.lemmatized(txtdf = txtdf, dir_saida = "/home/micael/R_envs/text-mining/dados/sbrt_txts/dossies_lematizados_subs/")


