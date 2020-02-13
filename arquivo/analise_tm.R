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
dados<-"~/dados/sbrt_txts/amostra_dossie/"

txtdf<-readtext::readtext(dados, encoding = "latin1")
txtdf$text<-sub('.*\nConteúdo',"",txtdf$text)
txtdf$text<-sub('.*\nCONTEÚDO',"",txtdf$text)
txtdf$text<-sub('.*\nTítulo',"",txtdf$text)
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
sbrt_sw <- c("http", "senai", "deve","acesso", "brasil", "devem", "pode", "ser","norma","iso", "kg", "fig", "fonte", "sbrt", "abnt", "nbr", "tecnica")
sw_pt <- c(sbrt_sw, sw_pt_tm)


# criar dataframe com uma linha por palavra
df_palavra <- txtdf %>% 
  unnest_tokens(palavra, text) %>% 
  # filtrar fora stopword
  filter(!palavra %in% sw_pt_tm)

df_palavra %>% 
  count(palavra) %>% 
  arrange(desc(n)) %>% 
  head(50) %>% 
  formattable()

sbrt_sw <- c("http", "senai", "deve","acesso", "brasil", "devem", "pode", "ser","norma","iso", "kg", "fig", "fonte", "sbrt", "abnt", "nbr", "tecnica")
sw_pt <- c(sbrt_sw, sw_pt_tm)

proc <- stm::textProcessor(txtdf$text, metadata = txtdf, language = "portuguese",
                           customstopwords = sw_pt)

out <- stm::prepDocuments(proc$documents, proc$vocab, proc$meta,
                          lower.thresh = 10)

storage <- stm::searchK(out$documents, out$vocab, K = c(3:15),
                        data = out$meta)
fit <- stm(
  documents = out$documents, vocab = out$vocab, data = out$meta,  K = 10,
  max.em.its = 75, init.type = "Spectral", verbose = FALSE
)

plot(fit, "summary")

head(fit$theta)


nomes_topicos <- c("1", "2", "3",
                   "4", "5", "6", "7",
                   "8", "9", "10")
# extrair a maior probabilidade pra cada documento
maior_prob <- apply(fit$theta, 1, max)
# extrair o nome do topico com a maior probabilidade
topico_doc <- nomes_topicos[apply(fit$theta, 1, which.max)]

# acrescentar esses dados no dataframe principal
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