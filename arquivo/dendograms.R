library(udpipe)
sbrt_sw <- c("http", "senai", "deve","acesso", "brasil","desenv.", 
             "devem", "pode", "ser","norma","iso", "kg","n.","p.", 
             "fig", "fonte", "sbrt", "abnt", "nbr", "tecnica","controle","qualidade",
             "sao", "c","pt.wikipedia.org","apresentar","resultado","mm","cm",
             "sopa","colher","minuto","hora","resposta","nao","temperatura",
             "ter","produto","processo","utilizar","agua","planta","producao")


topW <- sbrt_pos %>%      
  # (1) Use noun words from `upos`
  filter (upos %in% c("NOUN", "ADJ", "VERB")) %>%    
  # (2) Group by `lemma`
  group_by (lemma) %>%
  # (3) Count & sort lemma in descending order
  count (lemma, sort = TRUE) %>%
  # (4) Select columns by renaming `lemma`=>`Word` & `n`=>`Freq`
  select (Word = lemma, Freq = n) %>%  
  # (5) Then, ungroup them
  ungroup ()%>%
  filter(Freq >700)
sbrt_stw<-c(sbrt_sw,topW$Word)










cooc <- cooccurrence(x =subset(sbrt_pos, upos %in% c("NOUN", "VERB") & 
                                 !lemma %in% sbrt_stw), 
                     term = "lemma", 
                     group = c("doc_id", "paragraph_id", "sentence_id"))

library(igraph)
library(ggraph)
library(ggplot2)
wordnetwork <- head(cooc, 30)
wordnetwork <- graph_from_data_frame(wordnetwork)
ggraph(wordnetwork, layout = "fr") +
  geom_edge_link(aes(width = cooc, edge_alpha = cooc), edge_colour = "pink") +
  geom_node_text(aes(label = name), col = "darkgreen", size = 4) +
  theme_graph(base_family = "Arial Narrow") +
  theme(legend.position = "none") +
  labs(title = "Cooccurrences within sentence", subtitle = "Nouns & Adjective")



### Option 1: using ego-networks
V(wordnetwork) # the graph has 23 vertices
ego(wordnetwork, order = 2)# 2.0 level ego network for each vertex
ego(wordnetwork, order = 1, nodes = 10) # 1.0 level ego network for the 10th vertex (publico)




### Option 2: using community detection

# Community structure detection based on edge betweenness (http://igraph.org/r/doc/cluster_edge_betweenness.html)
wordnetwork1 <- as.undirected(wordnetwork) # an undirected graph

# Note that you can plot community object
comm <- cluster_edge_betweenness(wordnetwork1, weights = E(wordnetwork1)$cooc)
plot_dendrogram(comm)


# Community detection via random walks (http://igraph.org/r/doc/cluster_walktrap.html)

wordnetwork0<- as.undirected(wordnetwork) # an undirected graph

comm <- cluster_walktrap(wordnetwork0, weights = E(wordnetwork0)$cooc, steps = 2)
plot_dendrogram(comm)




# Community detection via optimization of modularity score
# This works for undirected graphs only
wordnetwork2 <- as.undirected(wordnetwork) # an undirected grap
# Note that you can plot community object
comm <- cluster_fast_greedy(wordnetwork2, weights = E(wordnetwork2)$cooc)
plot_dendrogram(comm)