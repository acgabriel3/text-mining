


metadados_sbrt<-metadados
metadados_web<-read_json("/home/micael/R_envs/text-mining/dados/sbrt_respostas_metadados.json")
metadados_web<-read_json(metadados_web)

for(i in 1:length(metadados_web)){
  metadados_web[[i]][["resposta"]]<-names(metadados_web[i])
  categorias<-unlist(metadados_web[[i]][["categoria"]], use.names = F)
  metadados_web[[i]][["categoria"]]<-NULL
  metadados_web[[i]][["categoria"]]<-paste(categorias,collapse=",")
  palavras<-unlist(metadados_web[[i]][["palavras_chave"]], use.names = F)
  metadados_web[[i]][["palavras_chave"]]<-NULL
  metadados_web[[i]][["palavras_chave"]]<-paste(palavras,collapse=",")
  rm(categorias)
  rm(palavras)
}

df_metadados <- data.frame(matrix(unlist(metadados_web), nrow=length(metadados_web), byrow=T))
names(df_metadados)<-names(metadados_web[[1]])

meta_web_df<- filter(df_metadados, data!="desconhecido", solicitacao!="desconhecido")%>%
  select(resposta,codigo_solicitacao, solicitacao)
names(meta_web_df)<-c("id", "codigo_solicitacao", "solicitacao")

meta_final<-merge(metadados_sbrt,meta_web_df,by="id")

write_csv(meta_final,"/home/micael/R_envs/text-mining/dados/sbrt_respostas_solicitacao_metadados.csv" )

