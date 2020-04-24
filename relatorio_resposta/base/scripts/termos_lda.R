

  dir_app<-"/home/sbrt/shiny/sbrt"
  setwd(dir_app)
  source("scripts/respostas/get_funs.R")
  options(java.parameters="-Xmx2g")
  library(dfrtopics)
  library(tidytext)
  library(tidyverse)
  library(mallet)
  library(dendextend)
  library(readr)
  
  #Diretórios dos arquivos necessários
  respostas_dir<-"/mnt/dados/sbrt/dados/sbrt_txts/respostas_txt/"
  #respostas_dir<-"/home/micael/R_envs/text-mining/dados/sbrt_txts/respostas_txt"
  metadados_dir<-"/mnt/dados/sbrt/metadados/metadados_RT.csv"
  stop_words_sbrt<-"/mnt/dados/sbrt/metadados/stop_words_sbrt.txt"
  
  
  
  
  docs_interesse<-paste0(respostas_dir,respostas_tbl()$document,".txt")
  
  #Leitura das stopwords.
  sw<-readr::read_lines(stop_words_sbrt)
  
  #Leitura e pré-processamento dos documentos.
  txtdf<-get_txt(docs_interesse)
  
  #Criação de um dataframe dos metadados dos documentos.
  metadados<-readr::read_csv2(metadados_dir)
  
  #Preaparação dos documentos para criação do modelo LDA.
  instance_mallet<-make_instances(txtdf, stoplist_file = stop_words_sbrt)
  
  
  #Criação do modelo LDA de acordo com o número de tópicos encontrado no processo anterior.
  best_model<-train_model(instance_mallet,n_topics = 1, metadata = metadados, seed = 12345)
  best_model$doc_ids<-doc_ids(best_model)
  
  
  #Gera dataframe de termos por tópico.
  terms_sbrt_filtered<-tidy(best_model$model, matrix = "beta")%>%
    arrange(desc(beta))
  
  terms_sbrt_filtered%>%select(-topic)
