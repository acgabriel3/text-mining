#faz todo o pre-processamento, tratamento de dados, 
#gera todos as informações necessárias para as visualizações
#e exporta um arquivo .RData para ser importado no dashboard

setwd("/home/sbrt/shiny/sbrt/")
options(java.parameters=c("-XX:+UseConcMarkSweepGC","-Xmx10g"))
source("relatorio_resposta/base/get_funs.R")
#library(dfrtopics)
library(tidytext)
library(tidyverse)
#library(mallet)
library(dendextend)
library(readr)

#Diretórios dos arquivos necessários
dosies_dir<-"/mnt/dados/sbrt/dados/sbrt_txts/dossies_txtv1"
metadados_dir<-"/mnt/dados/sbrt/metadados/metadados_DT_CNAE.csv"
stop_words_sbrt<-"/mnt/dados/sbrt/metadados/stop_words_sbrt.txt"

#Leitura das stopwords.
sw<-readr::read_lines(stop_words_sbrt)

#Leitura e pré-processamento dos documentos.
txtdf<-get_txt(dosies_dir)

#Criação de um dataframe dos metadados dos documentos.
metadados<-readr::read_csv2(metadados_dir)

#Criação de um datraframe apenas com os documentos e seus respectivos identificadores.
txtdf<-select(txtdf, id, text)

#Preaparação dos documentos para criação do modelo LDA.
instance_mallet<-make_instances(txtdf, stoplist_file = stop_words_sbrt)

#Busca pelo número de tópicos adequado para geração do modelo LDA.
#De acordo com a quantidade de documentos foi definido 60 como numero máximo de tópicos.
best_topic_dossies<-find_n_topics(txtdf,instance_mallet,stop_words= sw,metadados,max_topics=80,limites=10)

#Criação do modelo LDA de acordo com o número de tópicos encontrado no processo anterior.
best_model_dossies<-train_model(instance_mallet,n_topics = best_topic_dossies, metadata = metadados, seed = 12345)
best_model_dossies$doc_ids<-doc_ids(best_model_dossies)

#Extração dos rótulos dos tópicos.
labels_topics_dossies<-topic_labels(best_model_dossies, n=5)
labels_topics_selector_dossies<-topic_labels(best_model_dossies, n=3)

#Gera dataframe de documentos por tópico.
documents_sbrt_dossies<-tidy(best_model_dossies$model, matrix = "gamma")%>%
  arrange(desc(gamma))

#Insere os metadados no dataframe gerado no passo anterior e  seleciona os documentos mais relevantes.
dossies_topic<-metadados %>%
  mutate(document=id)%>%
  merge(documents_sbrt_dossies)%>%
  select(-id)%>%
  arrange(desc(gamma))%>%
  group_by(topic)


#Gera dataframe de termos por tópico.
terms_sbrt_dossies<-tidy(best_model_dossies$model, matrix = "beta")%>%
  arrange(desc(beta))


#Seleção dos doissiês mais relevantes por tópico.
dossies_topic<-dossies_topic %>%
  group_by(topic)%>%filter(gamma>0.1)%>%
  select(document, INST,
         CNAE_MACRO,CNAE_DESCR, TITULO_DT,
         DESCR_DOSSIE, DATA_CRIACAO, gamma,topic)

dossies_topic$periodo<-gsub(regex("(\\d+/\\d+/)", dotall = TRUE),"",dossies_topic$DATA_CRIACAO)%>%
  as.numeric()

#Seleção dos termos mais relevantes por tópico.
names(terms_sbrt_dossies)<-c("topic", "term", "beta")
terms_sbrt_dossies<-terms_sbrt_dossies%>%
  group_by(topic) %>% 
  #slice(1:1000)%>%
  #filter(beta>0.00015)%>%
  ungroup()


dossies_total<-nrow(dossies_topic)
periodo_dossies<- dossies_topic$periodo%>%unique()%>%sort()
topics_selector_dossies<-as.list(1:length(labels_topics_selector_dossies))
names(topics_selector_dossies)<-labels_topics_selector_dossies

#Criação do dendrograma de documentos
dendrograma_docs_dossies<-cluster.mallet(best_model_dossies, method = "ward.D", by="doc")%>%
  as.dendrogram(hang = -1, cex = 0.06)



par(mar = c(0,0,0,0))
dendrograma_docs_dossies %>% 
  set("branches_k_color", k = best_topic_dossies)%>% 
  set("labels_cex", 1) %>%
  set("leaves_cex",0.2)%>%
  set("hang_leaves",0.2)%>%
  set("branches_lwd", 2)%>%
  plot(horiz=T, axes=F)


#Criação do dendrograma de termos
dendrograma_terms_dossies<-cluster.mallet(best_model_dossies, method = "ward.D", by="term")%>%
  as.dendrogram(hang = -1, cex = 0.06)



par(mar = c(0,0,0,0))
dendrograma_terms_dossies %>% 
  set("branches_k_color", k = best_topic_dossies)%>% 
  set("labels_cex", 1) %>%
  set("leaves_cex",0.2)%>%
  set("hang_leaves",0.2)%>%
  set("branches_lwd", 2)%>%
  plot(horiz=T, axes=F)

jsonlda_dossies<-makeLDAvis(best_model_dossies$model)
cat(jsonlda_dossies, file =file.path("/var/www/html/DT","lda.json"))

metadados_dossies<-metadados
#Armazena os objetos necessários para a visualização no dashboard.
save(best_topic_dossies,
     dossies_topic,
     documents_sbrt_dossies,
     terms_sbrt_dossies,
     dendrograma_docs_dossies,
     dendrograma_terms_dossies,
     metadados_dossies,
     labels_topics_selector_dossies,
     topics_selector_dossies,
     periodo_dossies,
     file="/home/sbrt/dados/sbrt/dados/Rdata/sbrt_vis_20_dossies.RData")
     #file = paste0("relatorio_resposta/base/","sbrt_vis_",best_topic_dossies,"_dossies",".RData"))

save(best_model_dossies, file="modelo_dossies_20.RData")

