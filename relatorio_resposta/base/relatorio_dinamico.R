#faz todo o pre-processamento, tratamento de dados, 
#gera todos as informações necessárias para as visualizações
#e exporta um arquivo .RData para ser importado no dashboard

options(java.parameters =  "-Xmx12g")
library(rJava)
setwd("/home/sbrt/shiny/sbrt/")
#options(java.parameters="-Xmx10g")
source("scripts/respostas/get_funs.R")
#library(dfrtopics)
library(tidytext)
library(tidyverse)
options(java.parameters =  "-Xmx12g")
#library(mallet)
library(dendextend)
library(readr)

#Diretórios dos arquivos necessários
respostas_dir<-"/dados/dados_sbrt/sbrt_txts/respostas_txt"
#respostas_dir<-"/home/micael/R_envs/text-mining/dados/sbrt_txts/respostas_txt"
metadados_dir<-"/dados/dados_sbrt/metadados_RT_CNAE.csv"
stop_words_sbrt<-"/dados/dados_sbrt/stop_words_sbrt.txt"

#Leitura das stopwords.
sw<-readr::read_lines(stop_words_sbrt)

#Criação de um dataframe dos metadados dos documentos.
metadados<-readr::read_csv2(metadados_dir)
metadados$CNAE_MACRO<-as.factor(metadados$CNAE_MACRO)

#Selecionando  uma amostra 50% do total de documentos de cada CNAE macro 
amostra<-metadados%>%
  group_by(CNAE_MACRO)%>%
  sample_frac(.5)

#listando todas as respostas disponíveis
resposta_base<-data.frame(id=list.files(respostas_dir))
amostra_doc<-paste0(amostra$id,".txt")

#selecionando apenas as respostas da amostra
docs_interesse<-filter(resposta_base, id %in% amostra_doc)
docs_interesse<-paste0(respostas_dir,"/",docs_interesse$id)

#Leitura e pré-processamento dos documentos.
txtdf<-get_txt(docs_interesse)



#Criação de um datraframe apenas com os documentos e seus respectivos identificadores.
txtdf<-select(txtdf, id, text)

#Preaparação dos documentos para criação do modelo LDA.
instance_mallet<-make_instances(txtdf, stoplist_file = stop_words_sbrt)

#Busca pelo número de tópicos adequado para geração do modelo LDA.
#De acordo com a quantidade de documentos foi definido 200 como numero máximo de tópicos.
best_topic<-find_n_topics(txtdf,instance_mallet,stop_words= sw,metadados, 200)



txtdf<-get_txt(respostas_dir)



#Criação de um datraframe apenas com os documentos e seus respectivos identificadores.
txtdf<-select(txtdf, id, text)

#Preaparação dos documentos para criação do modelo LDA.
instance_mallet<-make_instances(txtdf, stoplist_file = stop_words_sbrt)


#Criação do modelo LDA de acordo com o número de tópicos encontrado no processo anterior.
best_model<-train_model(instance_mallet,n_topics = best_topic, metadata = metadados, seed = 12345)
best_model$doc_ids<-doc_ids(best_model)

#Extração dos rótulos dos tópicos.
labels_topics<-topic_labels(best_model, n=5)
labels_topics_selector<-topic_labels(best_model, n=3)

#Gera dataframe de documentos por tópico.
documents_sbrt<-tidy(best_model$model, matrix = "gamma")%>%
  arrange(desc(gamma))

#Insere os metadados no dataframe gerado no passo anterior e  seleciona os 100 documentos mais relevantes.
respostas_topic<-metadados %>%
  #dplyr::select(id, titulo, categoria, assunto)%>%
  mutate(document=id)%>%
  merge(documents_sbrt)%>%
  select(-id)%>%
  arrange(desc(gamma))%>%
  group_by(topic) #%>% slice(1:100)


#Gera dataframe de termos por tópico.
terms_sbrt<-tidy(best_model$model, matrix = "beta")%>%
  arrange(desc(beta))

#Criação do dendrograma de documentos
dendrograma_docs<-cluster.mallet(best_model, method = "ward.D", by="doc")%>%
  as.dendrogram(hang = -1, cex = 0.06)



par(mar = c(0,0,0,0))
dendrograma_docs %>% 
  set("branches_k_color", k = best_topic)%>% 
  set("labels_cex", 1) %>%
  set("leaves_cex",0.2)%>%
  set("hang_leaves",0.2)%>%
  set("branches_lwd", 2)%>%
  plot(horiz=T, axes=F)


#Criação do dendrograma de termos
dendrograma_terms<-cluster.mallet(best_model, method = "ward.D", by="term")%>%
  as.dendrogram(hang = -1, cex = 0.06)



par(mar = c(0,0,0,0))
dendrograma_terms %>% 
  set("branches_k_color", k = best_topic)%>% 
  set("labels_cex", 1) %>%
  set("leaves_cex",0.2)%>%
  set("hang_leaves",0.1)%>%
  set("branches_lwd", 2)%>%
  plot(horiz=T, axes=F)

jsonlda<-makeLDAvis(best_model$model,outDir = paste0("/home/sbrt/shiny/sbrt/relatorio_resposta/ldavis/",best_topic))



#Seleção das respostas mais relevantes por tópico.
respostas_topic<-respostas_topic %>%
  group_by(topic)%>%filter(gamma>0.1)%>%
  select(document,UF_ORIG, INST,
         CNAE_MACRO,CNAE_SUB_DESCR, TITULO_RT,
         DESCR_RT, DATA_CRIACAO, gamma,topic,AUTOR_QT,COD_QT,CNAE_SUB_RT)

respostas_topic$periodo<-gsub(regex("(\\d+/\\d+/)", dotall = TRUE),"",respostas_topic$DATA_CRIACAO)%>%
  as.numeric()

#Seleção dos termos mais relevantes por tópico.
names(terms_sbrt)<-c("topic", "term", "beta")
terms_sbrt<-terms_sbrt%>%
  group_by(topic) %>% 
  #slice(1:1000)%>%
  filter(beta>0.00015)%>%
  ungroup()


respostas_total<-nrow(respostas_topic)
periodo<- respostas_topic$periodo%>%unique()%>%sort()
topics_selector<-as.list(1:length(labels_topics_selector))
names(topics_selector)<-labels_topics_selector


#Armazena os objetos necessários para a visualização no dashboard.
save(best_topic,respostas_topic,terms_sbrt,respostas_total,dendrograma_docs,dendrograma_terms,periodo,metadados,labels_topics_selector,topics_selector,jsonlda, file = paste0("relatorio_resposta/base/","sbrt_vis_final_respostas",best_topic,".RData"),compress=FALSE)

