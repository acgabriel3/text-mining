library(tm)
library(readxl)
library(tm)
library(qdap)
library(wordcloud)
library(RColorBrewer)
library(stringr)
library(dplyr)
library(udpipe)
library(readr)
source("CRISPDM.R")
#options("encoding" = "UTF-8")

variaveis <- leitura_automatica_por_tipo_arquivo(diretorioAlvo = "~/dados/sbrt_txts/dossies", formatoArquivo = ".txt",
                                                 funcao_de_leitura = "readLines")

textoUnico <- NULL

for(i in 1) {
  
  textoUnico <- c(textoUnico, eval(as.symbol(variaveis[15])))
  
}

#Ajustando a codificação para evitar problemas com acentos e caracteres especiais
textoUnico<-iconv(textoUnico, from = "ISO-8859-1", to = "UTF-8")

#Leitura do texto bruto
txt<-read_file("~/dados/sbrt_txts/dossies/9056.txt")%>%
  iconv(from = "ISO-8859-1", to = "UTF-8")

#Tentativa de limpeza
#Remove folha de rosto, sumário etc.
txt<-sub('.*\r\nConteúdo', '', txt)%>%
  gsub('\"x\".*"\fTítulo\"','',.)%>%
  #remove numeração de linhas
  gsub('\\r\\n\"[1-9][0-9]*\"','',.)%>%
  gsub('\\"\\r\\n\"[1-9][0-9]*\"','',.)%>%
  gsub('"\\r\\n\"[1-9][0-9]*\"','',.)%>%
  #remove numeração de paágnas e rodapé
  gsub('\"\" \"Copyright © Serviço Brasileiro de Respostas Técnicas - SBRT - http://www.sbrt.ibict.br\" \"\" \"[1-9][0-9]*\" \"\" \"\f','',.)%>%
  #remove quebra de linha e aspas
  gsub("\\r\\n", "", .)%>%
  gsub('\"', "", .)


###############
#stri_enc_detect(`18.txt`)
#teste<-iconv(`18.txt`, from = "ISO-8859-1", to = "UTF-8")

#write.table(textoUnico, file="txt10.txt")
#library(readr)
#txt<-read_file("teste.txt")
#################

#Faz o download e carrega o modelo.
ud_model <- udpipe_download_model(language = "portuguese")
ud_model <- udpipe_load_model(ud_model$file_model)
#Faz anotação com base no modelo
x <- udpipe_annotate(ud_model, x = txt)
x <- as.data.frame(x)

#gera gŕafico de ocorrência de cada tipo de POS
library(lattice)
stats <- txt_freq(x$upos)
stats$key <- factor(stats$key, levels = rev(stats$key))
barchart(key ~ freq, data = stats, col = "cadetblue", 
         main = "UPOS (Universal Parts of Speech)\n frequency of occurrence", 
         xlab = "Freq")

#gera gŕafico de ocorrência de cada tipo de substantivo
stats <- subset(x, upos %in% c("NOUN")) 
stats <- txt_freq(stats$token)
stats$key <- factor(stats$key, levels = rev(stats$key))
barchart(key ~ freq, data = head(stats, 20), col = "cadetblue", 
         main = "Most occurring nouns", xlab = "Freq")

#gera gŕafico de ocorrência de cada tipo de adjvetivo
stats <- subset(x, upos %in% c("ADJ")) 
stats <- txt_freq(stats$token)
stats$key <- factor(stats$key, levels = rev(stats$key))
barchart(key ~ freq, data = head(stats, 20), col = "cadetblue", 
         main = "Most occurring adjectives", xlab = "Freq")

#identificação de palavras chave com o algoritimo RAKE
stats <- keywords_rake(x = x, term = "lemma", group = "doc_id", 
                       relevant = x$upos %in% c("NOUN", "ADJ"))
stats$key <- factor(stats$keyword, levels = rev(stats$keyword))
barchart(key ~ rake, data = head(subset(stats, freq > 3), 20), col = "cadetblue", 
         main = "Keywords identified by RAKE", 
         xlab = "Rake")

#identificação de palavras chave com o algoritimo PMI de colocações
x$word <- tolower(x$token)
stats <- keywords_collocation(x = x, term = "word", group = "doc_id")
stats$key <- factor(stats$keyword, levels = rev(stats$keyword))
barchart(key ~ pmi, data = head(subset(stats, freq > 3), 20), col = "cadetblue", 
         main = "Keywords identified by PMI Collocation", 
         xlab = "PMI (Pointwise Mutual Information)")

#identificação de palavras chave apartir de frases
## Using a sequence of POS tags (noun phrases / verb phrases)
x$phrase_tag <- as_phrasemachine(x$upos, type = "upos")
stats <- keywords_phrases(x = x$phrase_tag, term = tolower(x$token), 
                          pattern = "(A|N)*N(P+D*(A|N)*N)*", 
                          is_regex = TRUE, detailed = FALSE)
stats <- subset(stats, ngram > 1 & freq > 3)
stats$key <- factor(stats$keyword, levels = rev(stats$keyword))
barchart(key ~ freq, data = head(stats, 20), col = "cadetblue", 
         main = "Keywords - simple noun phrases", xlab = "Frequency")

#calcula coocorrência entre substantivos  e adjvetivos
cooc <- cooccurrence(x = subset(x, upos %in% c("NOUN", "ADJ")), 
                     term = "lemma", 
                     group = c("doc_id", "paragraph_id", "sentence_id"))
head(cooc)

library(igraph)
library(ggraph)
library(ggplot2)
wordnetwork <- head(cooc, 10)
wordnetwork <- graph_from_data_frame(wordnetwork)
ggraph(wordnetwork, layout = "fr") +
  geom_edge_link(aes(width = cooc, edge_alpha = cooc), edge_colour = "pink") +
  geom_node_text(aes(label = name), col = "darkgreen", size = 4) +
  theme_graph(base_family = "Arial Narrow") +
  theme(legend.position = "none") +
  labs(title = "Cooccurrences within sentence", subtitle = "Nouns & Adjective")

cooc <- cooccurrence(x$lemma, relevant = x$upos %in% c("NOUN", "ADJ"), skipgram = 1)
wordnetwork <- head(cooc, 50)
wordnetwork <- graph_from_data_frame(wordnetwork)
ggraph(wordnetwork, layout = "fr") +
  geom_edge_link(aes(width = cooc, edge_alpha = cooc)) +
  geom_node_text(aes(label = name), col = "darkgreen", size = 4) +
  theme_graph(base_family = "Arial Narrow") +
  labs(title = "Words following one another", subtitle = "Nouns & Adjective")

x$id <- unique_identifier(x, fields = c("sentence_id", "doc_id"))
dtm <- subset(x, upos %in% c("NOUN", "ADJ"))
dtm <- document_term_frequencies(dtm, document = "id", term = "lemma")
dtm <- document_term_matrix(dtm)
dtm <- dtm_remove_lowfreq(dtm, minfreq = 5)
termcorrelations <- dtm_cor(dtm)
y <- as_cooccurrence(termcorrelations)
y <- subset(y, term1 < term2 & abs(cooc) > 0.2)
y <- y[order(abs(y$cooc), decreasing = TRUE), ]
head(y)

#identificação de palavras chave com o algoritimo textrank
library(textrank)
stats <- textrank_keywords(x$lemma, 
                           relevant = x$upos %in% c("NOUN", "ADJ"), 
                           ngram_max = 8, sep = " ")
stats <- subset(stats$keywords, ngram > 1 & freq >= 5)
wordcloud(words = stats$keyword, freq = stats$freq)

stats <- keywords_rake(x = x, 
                       term = "token", group = c("doc_id", "paragraph_id", "sentence_id"),
                       relevant = x$upos %in% c("NOUN", "ADJ"),
                       ngram_max = 4)
head(subset(stats, freq > 3))

x$phrase_tag <- as_phrasemachine(x$upos, type = "upos")
stats <- keywords_phrases(x = x$phrase_tag, term = x$token, 
                          pattern = "(A|N)+N(P+D*(A|N)*N)*", 
                          is_regex = TRUE, ngram_max = 4, detailed = FALSE)
head(subset(stats, ngram > 2))

stats <- merge(x, x, 
               by.x = c("doc_id", "paragraph_id", "sentence_id", "head_token_id"),
               by.y = c("doc_id", "paragraph_id", "sentence_id", "token_id"),
               all.x = TRUE, all.y = FALSE, 
               suffixes = c("", "_parent"), sort = FALSE)
stats <- subset(stats, dep_rel %in% "nsubj" & upos %in% c("NOUN") & upos_parent %in% c("ADJ"))
stats$term <- paste(stats$lemma_parent, stats$lemma, sep = " ")
stats <- txt_freq(stats$term)
library(wordcloud)
wordcloud(words = stats$key, freq = stats$freq, min.freq = 3, max.words = 100,
          random.order = FALSE, colors = c("#1B9E77", "#D95F02", "#7570B3", "#E7298A", "#66A61E", "#E6AB02"))



##Não terminado
#Modelo de identificação de tópicos

dtf <- subset(x, upos %in% c("NOUN", "ADJ") & 
                !lemma %in% c("appartement", "appart", "eter", "tres"))
dtf <- document_term_frequencies(dtf, document = "topic_level_id", term = "lemma")
dtm <- document_term_matrix(x = dtf)
dtm_clean <- dtm_remove_lowfreq(dtm, minfreq = 5)

m <- LDA(dtm_clean, k = 4, method = "Gibbs", 
         control = list(nstart = 5, burnin = 2000, best = TRUE, seed = 1:5))
topicterminology <- predict(m, type = "terms", min_posterior = 0.025, min_terms = 5)
scores <- predict(m, newdata = dtm, type = "topics")

