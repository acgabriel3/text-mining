library(tm)
library(ggplot2)
library(ggthemes)
library(dplyr)
library(stringr)
dados<-"dados/sbrt_txts/amostra_dossie/"
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
sbrt_sw <- c("http", "senai", "deve","durante","acesso", "brasil", "devem", "pode", "ser","norma","iso", "kg", "fig", "fonte", "sbrt", "abnt", "nbr", "tecnica")
sw_pt <- c(sbrt_sw, sw_pt_tm)


clean.corpus<-function(corpus){
  corpus <- tm_map(corpus,content_transformer(tryTolower))
  corpus <- tm_map(corpus, removeWords,sbrt_stw)
  corpus <-tm_map(corpus, removePunctuation)
  corpus <-tm_map(corpus, stripWhitespace)
  corpus <- tm_map(corpus, removeNumbers)
  return(corpus)
}

corpus<-VCorpus(DataframeSource(txtdf))
corpus<-clean.corpus(corpus)

tdm<-TermDocumentMatrix(corpus, control = list(weighting= weightTf))
tdm.docs.m<-as.matrix(tdm)
term.freq<-rowSums(tdm.docs.m)
freq.df<-data.frame(word=names(term.freq), frequency=term.freq)
freq.df<-freq.df[order(freq.df[,2], decreasing=T),]

freq.df$word<-factor(freq.df$word,levels=unique(as.character(freq.df$word)))
ggplot(freq.df[1:20,], aes(x=word,y=frequency))+
  geom_bar(stat="identity",fill='darkred')+
  coord_flip()+
  theme_gdocs()+ 
  geom_text(aes(label=frequency),colour="white",hjust=1.25, size=5.0)


associations<-findAssocs(tdm, 'agua', 0.11)
associations<-as.data.frame(associations)
associations$terms<-row.names(associations)
associations$terms<-factor(associations$terms,levels=associations$terms)

library(igraph)
doc.adj<-tdm.docs.m %*% t(tdm.docs.m)
doc.adj<-graph.adjacency(doc.adj, weighted = T, mode="undirected", diag=T)
doc.adj<-simplify(doc.adj)


plot.igraph(doc.adj, vertex.shape="none",
            vertex.label.font=2, vertex.label.color="darkred",
            vertex.label.cex=.7, edge.color="gray85")
title(main='@DeltaAssist Refund Word Network')

