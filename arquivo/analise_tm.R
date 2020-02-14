options("encoding" = "UTF-8")
library(stringr)
library(tm)
library(SnowballC)
library(lexiconPT)
library(tidytext)
library(tidyverse)
library(magrittr)
library(stm)
library(ggridges)
library(formattable)
options(scipen = 999)
dados<-"/home/micael/R_envs/text-mining/dados/sbrt_txts/dossies"

#leitura de todos os dados do diretorio para um dataframe
txtdf<-readtext::readtext(dados, encoding = "latin1")

#tentativa de extração de informações sobre o documento
for (i in 1:length(txtdf$text)){
tx<-strsplit(x=txtdf[i,2], "\n")[[1]][2]
titulo[i]<-tx
}
txtdf$titulo<-titulo
tx<-tx[[1]]
i_titulo<-grep("Título",tx)
tx[i_titulo+1]
i_assunto<-grep("Assunto",tx)
tx[i_assunto+1]
i_resumo<-grep("Resumo", tx)
tx[i_resumo+1]
i_pchave<-grep("Palavras chave",tx)
tx[i_pchave+1]

titulo<-regmatches( txtdf[59,2], gregexpr("DOSSIÊ TÉCNICO.*.\n", txtdf[59,2], perl = F ) )
titulo

tes<-strsplit(tx, "Título ")
tes<-unlist(tes)

titulo<-regmatches( txtdf[358,2], gregexpr("(?<=Título ).*(?=Assunto)", txtdf[358,2], perl = TRUE ) )
titulo
assunto<-regmatches( txtdf[358,2], gregexpr("(?<=Assunto ).*(?= Resumo)", txtdf[358,2], perl = TRUE ) )
assunto
pchave<-regmatches( txtdf[358,2], gregexpr("(?<=Palavras-chave ).*(?=Conteúdo)", txtdf[358,2], perl = TRUE ) )
pchave

titulo<-regmatches( txtdf[38,2], gregexpr("(?=\nTítulo)", txtdf[358,2], perl = TRUE ) )
titulo
assunto<-regmatches( txtdf[38,2], gregexpr("(?<=Assunto ).*(?= Resumo)", txtdf[358,2], perl = TRUE ) )
assunto
pchave<-regmatches( txtdf[38,2], gregexpr("(?<=Palavras chave).*(?=Conteúdo)", txtdf[358,2], perl = TRUE ) )
pchave

#limpeza dos dados
txtdf$text<-sub('.*\nConteúdo',"",txtdf$text)
txtdf$text<-sub('.*\nCONTEÚDO',"",txtdf$text)
#txtdf$text<-sub('.*\nTítulo',"",txtdf$text)
txtdf$text<-sub('.*(?=\nTítulo)',"",txtdf$text,perl=T)
txtdf$text<-gsub('[1-9][0-9]* Copyright © Serviço Brasileiro de Respostas Técnicas - SBRT - http://www.sbrt.ibict.br',"",txtdf$text)
txtdf$text<-gsub('[1-9][0-9]* Copyright © Serviço Brasileiro de Respostas Técnicas - SBRT - http://www.respostatecnica.org.br',"", txtdf$text)
txtdf$text<-gsub('[1-9][0-9]*\nCopyright © Serviço Brasileiro de Respostas Técnicas - SBRT - http://www.respostatecnica.org.br',"", txtdf$text)
txtdf$text<-gsub('\nCopyright © Serviço Brasileiro de Respostas Técnicas - SBRT - http://www.sbrt.ibict.br\n\n[1-9][0-9]*',"", txtdf$text)
txtdf$text<-gsub('Disponível em: ',"",txtdf$text)
#txtdf$text<-gsub('<ht.*.>',"",txtdf$text)




txtdf$text<-str_replace_all(txtdf$text, "[^[:alnum:].:,?!;]", " ")
txtdf$text<-gsub("\\s+", " ", str_trim(txtdf$text))
txtdf$text<-gsub('Copyright Serviço Brasileiro de Respostas Técnicas SBRT http: www.respostatecnica.org.br [1-9][0-9]*',"",txtdf$text)

txtdf$text<-gsub('INTRODUÇÃO',"",txtdf$text)
txtdf$text<-gsub('Introdução',"",txtdf$text)

txtdf$text<- iconv(txtdf$text, from = "UTF-8", to = "ASCII//TRANSLIT")

# stopwords da lingua portuguesa sem acento
sw_pt_tm <- tm::stopwords("pt") %>% iconv(from = "UTF-8", to = "ASCII//TRANSLIT")
sbrt_sw <- c("http", "senai", "sbrt", "deve","acesso", "brasil", "devem", "pode", "ser","norma","iso", "kg", "fig", "fonte", "sbrt", "abnt", "nbr", "tecnica")
sw_pt <- c(sbrt_sw, sw_pt_tm)


# criar dataframe com uma linha por palavra
df_palavra <- txtdf %>% 
  unnest_tokens(palavra, text) %>% 
  # filtrar palavras diferentes das stopwords
  filter(!palavra %in% sw_pt_tm)

#apresenta palavras mais frequentes
df_palavra %>% 
  count(palavra) %>% 
  arrange(desc(n)) %>% 
  head(50) %>% 
  formattable()


#faz o processamento do texto
proc <- stm::textProcessor(txtdf$text, metadata = txtdf, language = "portuguese",
                           customstopwords = sw_pt_tm)

out <- stm::prepDocuments(proc$documents, proc$vocab, proc$meta,
                          lower.thresh = 10)

#storage <- stm::searchK(out$documents, out$vocab, K = c(3:3),
                      #data = out$meta)

#modelagem de tópicos (10 tópicos)
fit <- stm(
  documents = out$documents, vocab = out$vocab, data = out$meta,  K = 10,
  max.em.its = 75, init.type = "Spectral", verbose = FALSE
)
#grafico de tópicps
plot(fit, "summary")

#FREX apresenta as palavras que mais representam o tópico. 
stm::labelTopics(fit)

head(fit$theta)


nomes_topicos <- c("1", "2", "3",
                   "4", "5", "6", "7",
                   "8", "9", "10")
# extrai a maior probabilidade pra cada documento
maior_prob <- apply(fit$theta, 1, max)
# extrai o nome do topico com a maior probabilidade
topico_doc <- nomes_topicos[apply(fit$theta, 1, which.max)]

# acrescenta esses dados no dataframe principal
df_topico <- txtdf %>% 
  mutate(maior_prob = maior_prob,
         topico = topico_doc)



# grafico da quantidade de documentos por topico
roxo <- "mediumpurple4"
df_topico %>% 
  count(topico) %>% 
  # classificar em ordem decrescente
  mutate(topico = forcats::fct_reorder(topico, n)) %>% 
  ggplot(aes(x = topico, y = n)) + 
  geom_col(fill = roxo) +
  theme_minimal() + 
  labs(x = NULL, y = "Documentos",
       title = "Quantidade de documentos por tópico") +
  coord_flip()

#dataframe com nome do arquivo, titulo e tópico
topico_doc<-df_topico %>% 
  group_by(topico)%>%
  arrange(desc(maior_prob))%>%
  #filter(topico == 1)%>% 
  select(titulo,doc_id, topico, maior_prob)





#########################




























####################################
docs<-VectorSource(txtdf$text)
docs<-Corpus(docs)
docs <- tm_map(docs, content_transformer(removePunctuation))

for (i in 1:length(docs)){
  docs[[i]][["content"]] <- iconv(docs[[i]][["content"]], from = "UTF-8", to = "ASCII//TRANSLIT")
  #docs[[i]][["content"]] <- paste0(docs[[i]][["content"]], collapse = "\n")
}



##################################