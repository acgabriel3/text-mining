library(tm)
library(ggplot2)
library(ggthemes)
library(dplyr)
library(stringr)
library(skmeans)
library(cluster)
library(fpc)
library(clue)
library(wordcloud)
options(stringsAsFactors = F)
dados<-"~/dados/sbrt_txts/dossies/"
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

tryTolower <- function(x){
  y = NA
  try_error = tryCatch(tolower(x), error = function(e) e)
  if (!inherits(try_error, 'error'))
    y = tolower(x)
  return(y)
}



# stopwords da lingua portuguesa sem acento
sw_pt_tm <- tm::stopwords("pt") %>% iconv(from = "UTF-8", to = "ASCII//TRANSLIT")
sbrt_sw <- c("http", "senai", "deve","copyright","fone","fax","etal","agua","produto","durante","acesso", "brasil", "devem", "pode", "ser","norma","iso", "kg", "fig", "fonte", "sbrt", "abnt", "nbr", "tecnica")
sw_pt <- c(sbrt_sw, sw_pt_tm)


clean.corpus<-function(corpus){
  corpus <- tm_map(corpus,content_transformer(tryTolower))
  corpus <- tm_map(corpus, removeWords,sw_pt)
  corpus <-tm_map(corpus, removePunctuation)
  corpus <-tm_map(corpus, stripWhitespace)
  corpus <- tm_map(corpus, removeNumbers)
  return(corpus)
}

corpus<-VCorpus(DataframeSource(txtdf))
corpus<-clean.corpus(corpus)
#rm(txtdf)

doc.dtm<-DocumentTermMatrix(corpus, control=list(weighting= weightTfIdf))
#doc.dtm.m<-as.matrix(doc.dtm)
doc.dtm.s<-scale(doc.dtm,scale=T)
#doc.dtm.s[is.na(doc.dtm.s)] <- 0
doc.clusters<-kmeans(doc.dtm.s,3)

barplot(doc.clusters$size, main='k-means')
plotcluster(cmdscale(dist(doc.dtm)), doc.clusters$cluster)

  dissimilarity.m <- dist(doc.dtm.s)
plot(silhouette(doc.clusters$cluster, dissimilarity.m))

work.clus.proto<-t(cl_prototypes(doc.clusters))

comparison.cloud(work.clus.proto, max.words=50)

soft.part <- skmeans(doc.dtm, 50, m = 1.2, control = list(nruns = 5, verbose = T))

barplot(table(soft.part$cluster), main='Spherical k-means')

plotcluster(cmdscale(dist(doc.dtm)), soft.part$cluster)

plot(silhouette(soft.part))

s.clus.proto<-t(cl_prototypes(soft.part))
comparison.cloud(s.clus.proto, max.words = 100,scale=c(.7,.7), title.size=1)

sort(s.clus.proto[,1],decreasing=T)[1:5]
sort(s.clus.proto[,2],decreasing=T)[1:5]
sort(s.clus.proto[,3],decreasing=T)[1:5]
sort(s.clus.proto[,4],decreasing=T)[1:5]
sort(s.clus.proto[,5],decreasing=T)[1:5]
sort(s.clus.proto[,6],decreasing=T)[1:5]
sort(s.clus.proto[,7],decreasing=T)[1:5]
sort(s.clus.proto[,8],decreasing=T)[1:5]
sort(s.clus.proto[,8],decreasing=T)[1:5]


for (i in 1:50){
  print(sort(s.clus.proto[,i],decreasing=T)[1:5])
  print("//n")
}

